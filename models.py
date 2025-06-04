from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, plaintext_password):
        self.password = generate_password_hash(plaintext_password)

    def check_password(self, plaintext_password):
        return check_password_hash(self.password, plaintext_password)
    
class ClientDashboard(db.Model):
    __tablename__ = 'client_dashboard'
    
    id = db.Column(db.Integer, primary_key=True)
    client_code = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    investment_date = db.Column(db.Date)
    total_value = db.Column(db.Numeric(15,2))
    portfolio_value = db.Column(db.Numeric(15,2))
    return_pct = db.Column(db.Numeric(5,2))
    equity = db.Column(db.Numeric(15,2))
    mf = db.Column(db.Numeric(15,2))
    re = db.Column(db.Numeric(15,2))