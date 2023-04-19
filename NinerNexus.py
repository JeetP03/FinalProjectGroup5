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


@app.route("/")
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


@app.route('/addPost', methods=['GET', 'POST'])
def add_post(login_username):
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data   # grabs the file
        filename = file.filename    # gets the file name
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # saves the file

        # Stores file path for uploaded file
        directory = "static/postImageUpload"
        filepath = os.path.join(directory, filename)

        # Gets the username to be attached to the post from the database
        # mycursor = mydb.cursor()
        # mycursor.execute("SELECT username FROM users")
        # myresult = mycursor.fetchall()

       # for row in myresult:
       #     sql_username = (row[0])

        if request.method == 'POST':
            text = request.form['text']
            if not request.form['text']:
                flash('Please enter text', 'error')

            # Posts the username, text, and file path to the sql database
            else:
                post = AddPost(login_username, text, filepath)
                db.session.add(post)
                db.session.commit()
        return "File has been uploaded."
    return render_template('addPost.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    mycursor = mydb.cursor()
    if request.method == 'POST':
        if not request.form['username'] or not request.form['passwords']:
            flash('Please enter all the fields', 'error')
        else:
            # Check if any rows were returned with the inputted username
            try:
                mycursor.execute("SELECT username FROM users WHERE column_name = 'username'")
            except TypeError:
                # No rows were returned, so the value wasn't found
                flash('Username or password not found')
            else:
                # Traverse through the column and print each row
                for row in mycursor.fetchall():
                    login_username = (row[0])
                add_post(login_username)
                return "Login successful"
    return render_template("login.html")

if __name__ == '__main__':
    app.run(port=3304, host="localhost", debug=True)
