from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector as mysql
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"   # Change this in production

# ✅ Database connection
db = mysql.connect(
    host="localhost",
    user="root",
    password="Brithvik/1",  # ⚠️ keep secure in env later
    database="user_details"
)

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("welcome"))
    return render_template("login.html")

# ✅ User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM details WHERE email=%s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user["password"], password):
        session["user"] = user["email"]
        return jsonify({"success": True, "message": "✅ Login successful!"})
    else:
        return jsonify({"success": False, "message": "❌ Invalid email or password"})

# ✅ Signup Page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        cursor = db.cursor()
        cursor.execute("SELECT * FROM details WHERE email=%s", (email,))
        exists = cursor.fetchone()

        if exists:
            cursor.close()
            return jsonify({"success": False, "message": "⚠️ Email already registered"})

        hashed_pwd = generate_password_hash(password)
        cursor.execute("INSERT INTO details (email, password) VALUES (%s, %s)", (email, hashed_pwd))
        db.commit()
        cursor.close()
        return jsonify({"success": True, "message": "🎉 Registration successful! Please login."})

    return render_template("signup.html")

# ✅ Welcome Page
@app.route("/welcome")
def welcome():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("welcome.html", user=session["user"])

# ✅ Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    print("➡️ Starting Flask server with DB connection...")
    app.run(debug=True)
