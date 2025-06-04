from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl
import os
import smtplib
import random
from email.message import EmailMessage
from flask_sqlalchemy import SQLAlchemy
from models import db, User  


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql12782354:aTSPDpkmY9@sql12.freesqldatabase.com:3306/sql12782354'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#db = SQLAlchemy(app)

#FILE = "credentials.xlsx

@app.route('/register-user', methods=['POST'])
def register_user():
    data = request.get_json()
    # Check if username already exists
    existing_user = User.query.filter_by(username=data.get("username")).first()
    if existing_user:
        return jsonify({"status": "error", "message": "Username already exists"}), 409

    # Create a new User object
    new_user = User(
        email=data.get("email", ""),
        name=data.get("name", ""),
        client_id=data.get("clientId", ""),
        username=data.get("username", ""),
        #password=data.get("password", ""),
        role=data.get("role", "")
    )
    new_user.set_password(data.get("password", ""))  # ✅ hash the password
    # Add and commit to DB
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "User registered successfully!"})

@app.route('/validate-client', methods=['POST'])
def validate_client():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username, role="client").first()
    if user and user.check_password(password):
        return jsonify({"success": True, "client_id": user.client_id})
    else:
        return jsonify({"success": False, "message": "Invalid username or password"})
    
    
@app.route('/validate-login', methods=['POST'])
def validate_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    # Query the user from the database
    user = User.query.filter_by(username=username, role=role).first()

    if user and user.check_password(password):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "name": user.name,
            "client_id": user.client_id
        } for user in users
    ])


@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "Email not registered"})

    otp = str(random.randint(100000, 999999))

    # Save OTP temporarily in a file (for demo/testing purposes)
    with open("otp_store.txt", "w") as f:
        f.write(f"{email}:{otp}")

    # Send email
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = "harikahaari0914@gmail.com"
    msg["To"] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("harikahaari0914@gmail.com", "sxaftdirmrampoxx")  # ⚠️ Use env var in production
        server.send_message(msg)
        server.quit()
        return jsonify({"success": True})
    except Exception as e:
        print("Email error:", e)
        return jsonify({"success": False, "message": "Failed to send OTP"})
    
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data['email']
    entered_otp = data['otp']
    new_password = data['new_password']

    # Load saved OTP
    if not os.path.exists("otp_store.txt"):
        return jsonify({"success": False, "message": "No OTP found"})

    with open("otp_store.txt", "r") as f:
        content = f.read().strip()

    saved_email, saved_otp = content.split(":")

    if email != saved_email or entered_otp != saved_otp:
        return jsonify({"success": False, "message": "Invalid OTP"})

    # Update password in database
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found in database"})

    user.set_password(new_password)  # ✅ hash new password
    db.session.commit()

    return jsonify({"success": True})

@app.route('/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"success": False, "message": "User not found."})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"success": True, "message": "User deleted successfully."})

@app.route('/')
def home():
    return "Flask App is Running!"

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))  # Use Render's PORT or default 10000
    app.run(host="0.0.0.0", port=port, debug=False)
