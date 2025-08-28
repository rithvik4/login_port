from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",         # your MySQL username
    password="Brithvik/1",  # your MySQL password
    database="login_system"
)


@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("welcome"))
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"})

    hashed_password = generate_password_hash(password)

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        return jsonify({"success": True, "message": "Account created successfully!"})
    except mysql.connector.IntegrityError:
        return jsonify({"success": False, "message": "Email already exists!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        session["user"] = user["email"]
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})

@app.route("/welcome")
def welcome():
    if "user" in session:
        return render_template("home.html", email=session["user"])
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
