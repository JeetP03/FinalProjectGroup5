from flask import render_template, request, flash, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
import mysql.connector

# database info is local to computer
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

    def __init__(self, username, passwords):
        self.username = username
        self.passwords = passwords


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


@app.route("/feed")
def feed():
    return render_template("feed.html")


@app.route("/navigation")
def navigation():
    return render_template("navBar.html")


@app.route("/userProfile")
def user_profile():
    return render_template("userProfile.html")


@app.route('/addUser', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['passwords']:
            flash('Please enter all the fields', 'error')
        else:
            user = RegisterUser(request.form['username'], request.form['passwords'])

            db.session.add(user)
            db.session.commit()

            flash('User was successfully registered')
    return render_template('addUser.html')


@app.route('/addPost<string:login_username>', methods=['GET', 'POST'])
def add_post(currentUser):
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # grabs the file
        filename = file.filename    # gets the file name
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # saves the file

        # Stores file path for uploaded file
        directory = "static/postImageUpload"
        filepath = os.path.join(directory, filename)

        if request.method == 'POST':
            text = request.form['text']
            if not request.form['text']:
                flash('Please enter text', 'error')

            # Posts the username, text, and file path to the sql database
            else:
                post = AddPost(currentUser, text, filepath)
                db.session.add(post)
                db.session.commit()
        return "File has been uploaded."
    return render_template('addPost.html', form=form)

currentUser = "tempValue"


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        login_username = request.form['usern']
        login_password = request.form['passw']
        if not request.form['usern'] or not request.form['passw']:
            flash('Please enter all fields', 'error')
            return render_template("login.html")

        mycursor = mydb.cursor()
        global currentUser

        mycursor.execute(f"SELECT * FROM users WHERE username = '{login_username}' AND passwords = '{login_password}'")

        login_user = mycursor.fetchone()
        if login_user is not None:
            currentUser = login_username
            return redirect(url_for('feed'))
        else:
            flash('Account not found', 'error')

    return render_template("login.html")


if __name__ == '__main__':
    app.run(port=3304, host="localhost", debug=True)
