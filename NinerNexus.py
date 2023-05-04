from flask import render_template, request, flash, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import mysql.connector

# database info is local to computer database
DB_HOST = "localhost"
DB_NAME = "finalproject"
DB_USERNAME = "root"
DB_Password = "CLTnpase123$"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CLTnpase123$",
    database="finalproject"
)

database_file = f"mysql+pymysql://{DB_USERNAME}:{DB_Password}@{DB_HOST}:3306/{DB_NAME}"

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['UPLOAD_FOLDER'] = 'static/postImageUpload'

db = SQLAlchemy(app)


class RegisterUser(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    passwords = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(100), nullable=False)

    def __init__(self, username, passwords, bio):
        self.username = username
        self.passwords = passwords
        self.bio = bio


class AddPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    profile_username = db.Column(db.String(100), nullable=False)
    written_text = db.Column(db.String(100), nullable=False)
    media_location = db.Column(db.String(100), nullable=False)

    def __init__(self, profile_username, written_text, media_location):
        self.profile_username = profile_username
        self.written_text = written_text
        self.media_location = media_location


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route("/<login_username>")
def feed(login_username):
    static_url = url_for('static', filename='')
    feed_posts = AddPost.query.all()

    # Create an empty list to hold the post data
    posts = []

    for row in feed_posts:
        p_username = row.profile_username
        w_text = row.written_text
        m_location = row.media_location

        # Create a dictionary to hold the post data
        post_data = {'p_username': p_username, 'w_text': w_text, 'm_location': m_location}

        # Add the post to the list
        posts.append(post_data)

    return render_template('feed.html', login_username=login_username, posts=posts, static_url=static_url)


@app.route("/navigation")
def navigation():
    return render_template("navBar.html")


@app.route("/userProfile/<login_username>")
def user_profile(login_username):
    static_url = url_for('static', filename='')

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT bio FROM users WHERE username = '{login_username}'")
    user = mycursor.fetchone()
    user_bio = user[0]

    mycursor.execute(f"SELECT * FROM posts WHERE profile_username = '{login_username}'")
    user_post = mycursor.fetchall()

    # Create an empty list to hold the post data
    posts = []
    counter = 0

    for row in user_post:
        caption = row[2]
        image_path = row[3]
        image_location = image_path.replace("static/", "")
        counter = counter + 1

        # Create a dictionary to hold the post data
        post_data = {'caption': caption, 'image_location': image_location}

        # Add the post to the list
        posts.append(post_data)

    return render_template("userProfile.html", login_username=login_username, user_bio=user_bio,
                           static_url=static_url, posts=posts, counter=counter)


@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['passwords'] or not request.form['bio']:
            flash('Please enter all the fields', 'error')
        else:
            user = RegisterUser(request.form['username'], request.form['passwords'], request.form['bio'])

            db.session.add(user)
            db.session.commit()

            flash('User was successfully registered')
            return redirect(url_for('login'))

    return render_template('addUser.html')


@app.route('/addPost/<login_username>', methods=['GET', 'POST'])
def add_post(login_username):
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # grabs the file
        filename = file.filename  # gets the file name
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # saves the file

        # Stores file path for uploaded file
        directory = "static/postImageUpload"
        filepath = os.path.join(directory, filename)  # filename should not have any spaces

        if request.method == 'POST':
            text = request.form['text']
            if not request.form['text']:
                flash('Please enter text', 'error')

            # Posts the username, text, and file path to the sql database
            else:
                post = AddPost(login_username, text, filepath)
                db.session.add(post)
                db.session.commit()

                return redirect(url_for('feed', login_username=login_username))

    return render_template('addPost.html', form=form, login_username=login_username)


@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_username = request.form['usern']
        login_password = request.form['passw']
        if not request.form['usern'] or not request.form['passw']:
            flash('Please enter all fields', 'error')
            return render_template("login.html")

        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM users WHERE username = '{login_username}' AND passwords = '{login_password}'")
        login_user = mycursor.fetchone()

        if login_user is not None:

            user_profile(login_username)
            return redirect(url_for('feed', login_username=login_username))
        else:
            flash('Account not found', 'error')
    return render_template("login.html")


if __name__ == '__main__':
    app.run(port=3304, host="localhost", debug=True)
