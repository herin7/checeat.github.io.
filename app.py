import re  
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
from helpers import apology, login_required
import datetime


app = Flask(__name__)
app.debug = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

db = SQL("sqlite:///users.db")


@login_manager.user_loader
def load_user(user_id):
    return None 


@app.route("/")
def index():
    if "user_id" in session:
        return render_template("layout.html")
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        entered_password = request.form.get("password")
        name = request.form.get("username")

        if not name or not entered_password:
            return apology("Where are provide username and password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        if not rows or not check_password_hash(rows[0]["password"], entered_password):
            return apology("Invalid username or password", 403)
            
        else:
            session["user_id"] = rows[0]["id"]
            return redirect("/user_products")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        p1 = request.form.get("password")
        p2 = request.form.get("password2")
        name = request.form.get("username")

        if not re.match(r"^(?=.*[A-Za-z])[A-Za-z0-9]{3,}$", name):
            return apology("Username must contain letters, be at least 3 characters long, and not consist only of numbers", 400)

        if len(p1) < 3:
            return apology("Password must be at least 3 characters long", 400)

        if p1 != p2:
            return apology("Passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", name)
        if rows:
            return apology("Username already exists Try with anothr one!", 400)

        hash = generate_password_hash(p1)
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", name, hash)
        
        rows = db.execute("SELECT id FROM users WHERE username = ?", name)
        if rows:
            session["user_id"] = rows[0]["id"]
            return redirect("/user_products")
        else:
            return apology("User registration failed.Try again[it will work]")

    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        names = request.form.getlist("product_name[]")
        mfgs = request.form.getlist("manufacturing_date[]")
        exps = request.form.getlist("expiry_date[]")
        ptypes = request.form.getlist("product_type[]")

        for name, mfg, exp, ptype in zip(names, mfgs, exps, ptypes):
            if not name or not mfg or not exp or not ptype:
                flash("All fields are mandatory")
                return render_template("addfood.html")
            else:
                id = session["user_id"]
                db.execute("INSERT INTO products (user_id, product_name, manufacturing_date, expiry_date, product_type) VALUES (?, ?, ?, ?, ?)", id, name, mfg, exp, ptype)

        flash("Products Added")
        return redirect("/user_products")
    else:
        return render_template("addfood.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/deregister", methods=["GET", "POST"])
@login_required
def deregister():
    user_id = session["user_id"]
    db.execute("DELETE FROM products WHERE user_id = ?", user_id)
    db.execute("DELETE FROM users WHERE id = ?", user_id)
    session.clear()
    return redirect("/")


@app.route("/user_products")
@login_required
def user_products():
    user_id = session["user_id"]
    today = datetime.date.today()

    products = db.execute("SELECT * FROM products WHERE user_id = ? ORDER BY expiry_date ASC", user_id)
    
    one_month = today + datetime.timedelta(days=30)
    one_week = today + datetime.timedelta(days=7)
    one_day = today + datetime.timedelta(days=1)

    close_to_expiry = {'one_month': [], 'one_week': [], 'one_day': []}
    expired_products = []

    for product in products:
        expiry_date = datetime.datetime.strptime(product['expiry_date'], '%Y-%m-%d').date()

        if expiry_date <= today:
            expired_products.append(product)
        elif expiry_date <= one_day:
            close_to_expiry['one_day'].append(product)
        elif expiry_date <= one_week:
            close_to_expiry['one_week'].append(product)
        elif expiry_date <= one_month:
            close_to_expiry['one_month'].append(product)

    return render_template("user_products.html", close_to_expiry=close_to_expiry, expired_products=expired_products)


@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    db.execute("DELETE FROM products WHERE id = ?", product_id)
    return redirect('/user_products')


if __name__ == "__main__":
    app.run()
