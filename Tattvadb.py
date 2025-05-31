import openpyxl
from app import db, User, app
from werkzeug.security import generate_password_hash

def import_excel_to_db(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active

    try:
        with app.app_context():
            for row in ws.iter_rows(min_row=2, values_only=True):
                email, name, client_id, username, password, role = row

                if not role:
                    print(f"Skipping user {username} due to missing role.")
                    continue

                if not User.query.filter_by(username=username).first():
                    user = User(email=email, name=name, client_id=client_id,
                                username=username, role=role)
                    user.set_password(password)  # ✅ hash before storing
                    db.session.add(user)

            db.session.commit()
            print("✅ Data successfully imported from Excel to SQLite!")
    except Exception as e:
        db.session.rollback()
        print("❌ Error during import:", e)

import_excel_to_db("credentials.xlsx")
