from app import app
from flask import  render_template


@app.errorhandler(404)
def not_found(e):
    return render_template("error_handler_template/404.html")