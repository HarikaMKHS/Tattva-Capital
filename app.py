from flask import Flask, request, jsonify
import openpyxl
import os

app = Flask(__name__)
FILE = "credentials.xlsx"

@app.route('/save-to-excel', methods=['POST'])
def save_to_excel():
    data = request.get_json()
    file_exists = os.path.exists(FILE)

    if not file_exists:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Name", "Client ID", "Username", "Password"])
    else:
        wb = openpyxl.load_workbook(FILE)
        ws = wb.active

    ws.append([data["name"], data["clientId"], data["username"], data["password"]])
    wb.save(FILE)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
