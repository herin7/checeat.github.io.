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

# Initialize Flask LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize SQLite database
db = SQL("sqlite:///users.db")



# Define user loader for Flask LoginManager
@login_manager.user_loader
def load_user(user_id):
    # Function to load user from the database based on user_id
    return None  # Replace with your actual user loading logic



# Homepage - Shows options for logged-in or new users
@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html")  # Show options for logged-in users
    else:
        return render_template("register.html")  # Show options for new users (login/register)

# Login route
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # Authentication logic
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

# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Registration logic with password and username checks using regular expressions
        p1 = request.form.get("password")
        p2 = request.form.get("password2")
        name = request.form.get("username")

        if not re.match(r"^(?=.*[A-Za-z])[A-Za-z0-9]{3,}$", name):
            return apology("Username must contain letters, be at least 3 characters long, and not consist only of numbers", 400)

        # Password checks: must be at least 3 characters long
        if len(p1) < 3:
            return apology("Password must be at least 3 characters long", 400)

        if p1 != p2:
            return apology("Passwords do not match", 400)

        # Check if username already exists
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

# Adding products route
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # Adding products logic
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

# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear the session data
    return redirect("/")  # Redirect to the homepage after logout

# Deregister route
@app.route("/deregister", methods=["GET", "POST"])
@login_required
def deregister():
    # Deregistration logic - Delete user data from tables
    user_id = session["user_id"]
    db.execute("DELETE FROM products WHERE user_id = ?", user_id)
    db.execute("DELETE FROM users WHERE id = ?", user_id)
    session.clear()
    return redirect("/")





# User products route
@app.route("/user_products")
@login_required
def user_products():
    # Logic to fetch user's products, organize by expiry date, and display them
    user_id = session["user_id"]
    today = datetime.date.today()

    # Fetch products ordered by expiry date (closest first)
    products = db.execute("SELECT * FROM products WHERE user_id = ? ORDER BY expiry_date ASC", user_id)
    
    # Partition products by expiry date proximity (e.g., 1 day, 1 week, 1 month)
    one_month = today + datetime.timedelta(days=30)
    one_week = today + datetime.timedelta(days=7)
    one_day = today + datetime.timedelta(days=1)

    # Group products based on their proximity to expiry date
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
    # Here, you'd have your logic to delete the product from your database

    # Sample code to delete from a database using cs50 library
    db.execute("DELETE FROM products WHERE id = ?", product_id)

    # After deleting the product, you might want to redirect the user to a different page
    return redirect('/user_products')  # Redirect to the user products page after deletion


# Run the app
if __name__ == "__main__":
    app.run()

