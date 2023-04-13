from flask import render_template, request, flash, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy

# database info is local to computer
DB_HOST = "localhost"
DB_NAME = "finalproject"
DB_USERNAME = "root"
DB_Password = "CLTnpase123$"

database_file = f"mysql+pymysql://{DB_USERNAME}:{DB_Password}@{DB_HOST}:3306/{DB_NAME}"

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class RegisterUser(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    passwords = db.Column(db.String(100), nullable=False)

    def __init__(self, username, passwords):
        self.username = username
        self.passwords = passwords


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

if __name__ == '__main__':
    app.run(port=3304, host="localhost", debug=True)
