from datetime import datetime
from apps.app import db,login_manager
from flask_login import  UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
 
from apps.natyukatu.models import Title
 
class User(db.Model, UserMixin):
    """ユーザーテーブル"""
    __tablename__ = "users"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    emall = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    title_id = db.Column(db.Integer,db.ForeignKey("titles.id"))  # FK
    tancks_point = db.Column(db.String(20), nullable=False)
    ranking_id = db.Column(db.String(10))
    group_name = db.Column(db.String(20), nullable=False)
    representative_name = db.Column(db.String(10), nullable=False)
    contact_email = db.Column(db.String(11), nullable=False)
    gtoup_type = db.Column(db.String(20), nullable=False)

    users_title = db.relationship("Title", backref=db.backref("users",lazy=True))

    @property
    def password(self):
        raise AttributeError("読み取り不可")
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
 
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
   
    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None
   
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
 
 
 