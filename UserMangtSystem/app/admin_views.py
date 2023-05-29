from app import app
from .views import User

from flask import render_template , redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///admin.db"
app.config["SECRET_KEY"] = 'TPPAMUXzd1X0ldIvdTZacA'


# create the extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)




class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Admin '{self.username}'>"


db.create_all()

# one time username and password for admin

admin = Admin(username ="admin" , password = bcrypt.generate_password_hash("admin" , 10))
db.session.add(admin)
db.session.commit()



@app.route("/admin/admin_login", methods = [ "GET", "POST"] )
def admin_login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        print(username, password)

        if username =="" or password == "":
            flash("Please fill in your credentials", "danger")
            return redirect("/admin/admin_login")

        else:
            admins = Admin().query.filter_by(username = username).first()
            if admins and bcrypt.check_password_hash(admins.password, password):
            #login 
                session["admin_id"] = admins.id
                session["admin_username"] = admins.username
                flash("login in successfully", "success")

                return redirect("/admin/admin_dashboard")




    return render_template("admin/admin_login.html")


@app.route("/admin/admin_dashboard")
def admin_dashboard():

    users = User.query.all()
    return render_template("admin/admin_dashboard.html" , users = users)


@app.route("/admin/approve_user/<int:id>")
def approve_user(id):
    User().query.filter_by(id=id).update(dict(status=1))
    db.session.commit()
    flash("user approved successfully", "success")
    return redirect("/admin/admin_dashboard")




@app.route("/admin/admin_profile")
def admin_profile():
    return render_template("admin/admin_profile.html")



@app.route("/admin/admin_logout")
def admin_logout():
    if session.get("admin_id"):
        session["admin_id"] = None
        session["admin_username"] = None
  

    return redirect("/admin/admin_login")