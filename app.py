from flask import Flask, request, jsonify
from flask_cors import CORS
import openpyxl
import os
import smtplib
import random
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)
FILE = "credentials.xlsx"

@app.route('/save-to-excel', methods=['POST'])
def save_to_excel():
    data = request.get_json()
    file_exists = os.path.exists(FILE)
    headers = ["Email","Name", "Client ID", "Username", "Password", "role"]

    if not file_exists:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
    else:
        wb = openpyxl.load_workbook(FILE)
        ws = wb.active

        current_headers = [cell.value for cell in ws[1]]
        if current_headers!= headers:
            for i, header in enumerate(headers, start=1):
                ws.cell(row=1, column=i).value = header
            # ws.insert_cols(len(current_headers) + 1)
            # ws.cell(row=1, column=6).value = "role"
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[3] == data["username"]:  # Username is the 3rd column (index 2)
            return jsonify({"status": "error", "message": "Username already exists"}), 409
        
    ws.append([
        data.get("email", ""),
        data.get("name", ""),
        data.get("clientId", ""),
        data.get("username", ""),
        data.get("password", ""),
        data.get("role", "")
    ])
    #ws.append([data["email"],data["name"], data["clientId"], data["username"], data["password"],data["role"]])
    wb.save(FILE)
    return jsonify({"status": "success"})



@app.route('/validate-client', methods=['POST'])
def validate_client():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    wb = openpyxl.load_workbook("credentials.xlsx")
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):  # skip header
        email,name, client_id, saved_username, saved_password, role = row

        #if saved_username == username and saved_password == password and role.lower() == "client":
        if saved_username == username and saved_password == password and str(role).lower() == "client":
            return jsonify({"success": True})

    return jsonify({"success": False})

@app.route('/validate-login', methods=['POST'])
def validate_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    wb = openpyxl.load_workbook(FILE)
    ws = wb.active

    for row in ws.iter_rows(min_row=2, values_only=True):
        email,name, client_id, saved_username, saved_password,saved_role = row
        if (
            saved_username == username and
            saved_password == password and
            str(saved_role).lower() == str(role).lower()
        ):
            return jsonify({"success": True})
    return jsonify({"success": False})


@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data['email']
    wb = openpyxl.load_workbook(FILE)
    ws = wb.active

    found = False
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == email:
            found = True
            break

    if not found:
        return jsonify({"success": False, "message": "Email not registered"})

    otp = str(random.randint(100000, 999999))
    
    # Send email
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = "your_email@gmail.com"
    msg["To"] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login("your_email@gmail.com", "your_app_password")
        server.send_message(msg)
        server.quit()
        return jsonify({"success": True, "otp": otp})
    except Exception as e:
        print("Email error:", e)
        return jsonify({"success": False, "message": "Failed to send OTP"})


@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data['email']
    new_password = data['new_password']

    wb = openpyxl.load_workbook(FILE)
    ws = wb.active

    for row in ws.iter_rows(min_row=2):
        if row[0].value == email:
            row[4].value = new_password
            wb.save(FILE)
            return jsonify({"success": True})

    return jsonify({"success": False, "message": "Email not found"})


if __name__ == '__main__':
    app.run(debug=True)

