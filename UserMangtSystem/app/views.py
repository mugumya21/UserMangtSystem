
from app import app
import os
from flask import render_template , redirect, request, flash
from flask import send_from_directory , abort
from werkzeug.utils import secure_filename
from flask import session , url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///admin.db"

app.config["IMAGE_UPLOADS"] = "/Users/Vic/Desktop/PLEDGE_CARD/app/static/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPEG", "JPG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024
app.config["CLIENT_IMAGES"] = "/home/vic/Documents/PLEDGE_CARD/app/static/clients/img"
app.config["SECRET_KEY"] = 'TPPAMUXzd1X0ldIvdTZacA'




@app.route("/")
def index():


    return render_template("public/index.html")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    edu = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    status = db.Column(db.Integer, default= 0 , nullable=False)

    def __repr__(self):
        return f"<User is '{self.fname}', '{self.lname}' , '{self.edu}' , '{self.email}' , '{self.password}', '{self.status}'>"



db.create_all()


@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():

    if session.get("user_id"):
        return redirect("/dashboard")



    if request.method == "POST":

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        edu = request.form.get("edu")
        email = request.form.get("email")
        password = request.form.get("password")

        print(fname, lname, username, edu, email, password)

        if fname == "" or lname == "" or edu == "" or email == "" or username =="" or password == "":
            flash("Please fill all the fields ", "danger")

            return redirect("/sign_up")


            
        else:
            pw_hash = bcrypt.generate_password_hash(password , 10)
            user = User(fname = fname, lname = lname , username= username,  edu = edu , email = email , password = pw_hash)
            db.session.add(user)
            db.session.commit()
            flash("Account created, wait for 10 to 30 min for admin to approve  ", "success")
            return redirect("/sign_up")


    else:

        return render_template("public/sign_up.html")


@app.route("/login", methods= ["POST", "GET"])
def login():
    if session.get("user_id"):
        return redirect("/dashboard")


    if request.method == "POST":
        
        email = request.form.get("email")
        password = request.form.get("password")
        print( email , password)

        # check for them in db
        users = User().query.filter_by(email = email).first()
        if users and bcrypt.check_password_hash(users.password, password):
            

                session["user_id"] = users.id
                session["username"] = users.username
                flash("Login successfully ", "success")
                return redirect("/dashboard")

        else:

            flash("Invalid email or password ", "danger")
            return redirect("/login")

  

            return redirect("/login")

    else:

        return render_template("public/login.html", title = "login")


@app.route("/about")
def about():
    return render_template("public/about.html")


@app.route("/dashboard")
def dashboard():

    # if  not session.get("user_id"):
    #     return redirect("/")

   

    return render_template("public/dashboard.html")


@app.route("/logout")
def logout():
    if session.get("user_id"):
        session["user_id"] = None
        session['username'] = None

    return redirect("/login")




@app.route("/update_profile", methods =["POST"  , "GET"])
def update_profile():
    if not session.get("user_id"):
        return redirect('/')

    if request.method == "POST":

        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        edu = request.form.get("edu")
        email = request.form.get("email")
        password = request.form.get("password")

        print(fname, lname, username, edu, email, password)

        if fname == "" or lname == "" or edu == "" or email == "" or username =="" or password == "":
            flash("Please fill all the fields ", "danger")

        else:
            user = User.query.filter_by(email = email).first()
            if user:
                pw_hash = bcrypt.generate_password_hash(password , 10)
                User.query.filter_by(email = email).update(dict(fname= fname, lname = lname, username = username, edu = edu, email= email,  password = pw_hash))
                db.session.commit()
                flash("profile updated successfully", "success")
                return redirect("/update_profile")

    else:

        return render_template("public/update_profile.html")

@app.route("/change_password", methods = [ "GET", "POST"])
def change_password():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")


        if  email == "" and password == "":
            flash("Please fill all the fields ", "danger")

        else:
            user = User.query.filter_by(email = email).first()
            if user:
                pw_hash = bcrypt.generate_password_hash(password , 10)
                User.query.filter_by(email = email).update(dict(password = pw_hash))
                db.session.commit()
                flash("password updated successfully", "success")
    

    return render_template("public/change_password.html")



def allowed_image_filesize(filesize):
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def allowed_image(filename):

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True

    else:
        return False


@app.route("/upload_image", methods = ["GET", "POST"])
def upload_image():

    if request.method =="POST":

        if request.files:
            if not allowed_image_filesize(request.cookies.get("filesize")):
                print("The file has exceeded the maximum size ")

                return redirect(request.url)

            print(request.cookies)
            image = request.files["image"]

            if image.filename =="":
                print("The image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("That image extension is not allowed")

                return redirect(request.url)

            else:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("image saved successfully")

                return redirect(request.url)




    return render_template("public/upload_image.html")





'''
    string:
    path:
    int:
    uuid:
'''
@app.route("/get_image/<string:image_name>")

def get_image(image_name):


    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename = image_name , as_attachment = False)

    except FileNotFoundError:
        abort(404)

@app.route("/get_csv/<filename>")

def get_csv(filename):


    try:
        return send_from_directory(
            app.config["CLIENT_IMAGES"], filename = filename , as_attachment = True) #to download the csv file

    except FileNotFoundError:
        abort(404)


















