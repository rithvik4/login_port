from flask import Flask, render_template, request, jsonify
import mysql.connector 

app = Flask(__name__)

# ✅ Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Varun@1505",   # ⚠️ better to keep in config/env later
    database="user_detail"
)

@app.route("/")
def home():
    return render_template("login.html")   # make sure login.html exists in templates/

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM details WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"success": True, "message": "Login successful!"})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"})

@app.route("/welcome")
def welcome():
    return "<h1>Welcome! 🎉 🎉 🎉 🎉 🎉 You have logged in successfully 🎉 🎉 🎉 🎉 🎉 </h1>"

if __name__ == "__main__":
    print("➡️ Starting Flask server with DB connection...")
    app.run(debug=True)
