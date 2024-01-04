# ChecEat

ChecEat is a Flask-based application designed to assist users in managing perishable items like food and medicine. It sorts and organizes products based on their expiry dates, helping users consume or utilize them before expiration.

### Key Features

- **User Authentication:** Secure login and registration using hashed passwords.
- **Product Management:** Addition, deletion, and categorization of products by expiry date.
- **User-Friendly Interface:** Intuitive and simple UI for easy interaction.

### Setup

1. **Installation:**
   - Clone this repository.
   - Install dependencies using `pip install -r requirements.txt`.

2. **Run the Application:**
   - Start the Flask app using `python app.py` or `flask run`.
   - Access the application via your web browser at `http://localhost:5000`.

### Usage

1. **Registration/Login:**
   - New users can register with a username and password.
   - Existing users can log in securely to access the app's features.

2. **Adding Products:**
   - Users can add new items with manufacturing and expiry dates, along with the product type.

3. **Viewing Products:**
   - Products are categorized by their proximity to expiry dates (e.g., within a day, week, or month).

4. **Deleting Items:**
   - Remove items that have been consumed or discarded.

### Project Structure

- **`app.py`:** Contains the main Flask application logic, routing, and database operations.
- **`templates/`:** Holds HTML templates for various pages (login, registration, product addition, etc.).
- **`static/`:** Contains static files (CSS, JavaScript, images) for frontend styling.

### How It Works

- **Login/Register Routes:** Authentication logic for user login and registration.
- **Product Addition:** Allows users to add new products with relevant details.
- **Expiry Date Classification:** Organizes products based on their proximity to their expiry dates.
- **Product Deletion:** Enables users to remove items they no longer need.

### Technologies Used

- **Flask:** Python-based micro web framework for building web applications.
- **SQLAlchemy:** SQL toolkit and Object-relational mapping (ORM) for database interaction.
- **HTML/CSS/JavaScript:** Frontend development languages for UI/UX design and functionality.

### Contributing

- **Issues:** Feel free to report any issues or bugs.
- **Pull Requests:** Contributions and enhancements are welcome!
