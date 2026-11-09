from datetime import datetime
from flask_login import UserMixin
from apps.app import db
 
 
class Recruitment(db.Model):
    """募集テーブル"""
    __tablename__ = "recruitments"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("recruitment_tags.id"), nullable=False)
    location_prefecture = db.Column(db.String(5), nullable=False)
    location_city = db.Column(db.String(10), nullable=False)
    location_detail = db.Column(db.String(30), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False)
    end_at = db.Column(db.DateTime, nullable=False)
    application_start_at = db.Column(db.DateTime, nullable=False)
    application_end_at = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    eligibility = db.Column(db.String(30), nullable=False)
    required_items = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    review_status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
 
    user = db.relationship("User", back_populates="recruitments")
    favorites = db.relationship("Like", back_populates="recruitment")
    participants = db.relationship("Participants", back_populates="recruitment")
    view_histories = db.relationship("ViewHistory", back_populates="recruitment")
    tag = db.relationship("RecruitmentTag", back_populates="recruitments")
    search_tags = db.relationship("SearchTag", back_populates="recruitment")
    entries = db.relationship("Entry", back_populates="recruitment")
    thanks_points = db.relationship("ThanksPoint", back_populates="recruitment")
 
 
class Like(db.Model):
    """お気に入りテーブル"""
    __tablename__ = "likes"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
 
    user = db.relationship("User", back_populates="likes")
    recruitment = db.relationship("Recruitment", back_populates="likes")
 
 
class SearchHistory(db.Model):
    """検索履歴テーブル"""
    __tablename__ = "search_histories"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
     
    user = db.relationship("User", back_populates="search_histories")
    recruitment = db.relationship("Recruitment", back_populates="search_histories")
 
class ParticipationHistory(db.Model):
    """参加履歴テーブル"""
    __tablename__ = "participation_histories"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    user = db.relationship("User", back_populates="participation_histories")
    recruitment = db.relationship("Recruitment", back_populates="participation_histories")
     
 
class RecruitmentHistory(db.Model):
    """募集履歴テーブル"""
    __tablename__ = "recruitment_histories"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
   
    user = db.relationship("User", back_populates="recruitment_histories")
    recruitment = db.relationship("Recruitment", back_populates="recruitment_histories")
 
class Participants(db.Model):
    """参加者テーブル"""
    __tablename__ = "participants"
 
    id = db.Column(db.Integer, primary_key=True)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    participant_count = db.Column(db.Integer)
    varchar = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    applicant_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    cancel_at = db.Column(db.DateTime, nullable=False)
 
    user = db.relationship("User", back_populates="participations")
    recruitment = db.relationship("Recruitment", back_populates="participants")
 
 
class ViewHistory(db.Model):
    """閲覧履歴テーブル"""
    __tablename__ = "view_histories"

    id = db.Column(db.Integer, primary_key=True)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    added_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="view_histories")
    recruitment = db.relationship("Recruitment", back_populates="view_histories")
 
 
class RecruitmentTag(db.Model):
    """タグ管理用テーブル"""
    __tablename__ = "recruitment_tags"
 
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(20), nullable=False)
 
    recruitments = db.relationship("Recruitment", back_populates="tag")
    search_tags = db.relationship("SearchTag", back_populates="tag")
 
 
class SearchTag(db.Model):
    """タグ検索用テーブル"""
    __tablename__ = "search_tags"
 
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("recruitment_tags.id"), nullable=False)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
 
    tag = db.relationship("RecruitmentTag", back_populates="search_tags")
    recruitment = db.relationship("Recruitment", back_populates="search_tags")
 
 
class Title(db.Model):
    """称号テーブル"""
    __tablename__ = "titles"
 
    id = db.Column(db.Integer, primary_key=True)
    title_name = db.Column(db.String(20), nullable=False)
    title_explanation = db.Column(db.String, nullable=False)
 
 
class Entry(db.Model):
    """申込者テーブル"""
    __tablename__ = "entries"
 
    id = db.Column(db.Integer, primary_key=True)
    recruitment_id = db.Column(db.Integer, db.ForeignKey("recruitments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    message = db.Column(db.Text)
    status = db.Column(db.String(10), nullable=False)
    applicant_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    cansel_at = db.Column(db.DateTime, nullable=False)
 
    user = db.relationship("User", back_populates="entries")
    recruitment = db.relationship("Recruitment", back_populates="entries")
 
 
class ActiveMessage(db.Model):
    """活動用メッセージテーブル"""
    __tablename__ = "active_messages"
 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    post_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
 
 
class ThanksPoint(db.Model):
    """サンクスポイントテーブル"""
    __tablename__ = "thanks_points"
 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    point_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
 
    user = db.relationship("User", back_populates="thanks_points")
    recruitment = db.relationship("Recruitment", back_populates="thanks_points")
 
#ランキングテーブル(いらんかも) 
#class Ranking(db.Model):
#    __tablename__ = "rankings"
 
#    id = db.Column(db.Integer, primary_key=True)

class ContactHistory(db.Model):
    """お問い合わせ履歴テーブル"""
    __tablename__ = "contact_histories"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
 
    user = db.relationship("User", back_populates="contact_histories")