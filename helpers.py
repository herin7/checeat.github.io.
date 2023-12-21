# helpers.py
from flask import redirect, session, flash,render_template
from functools import wraps
import datetime
from cs50 import SQL

db = SQL("sqlite:///users.db")


def apology(message, code=400):
    return render_template("apology.html", message=message), code



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

