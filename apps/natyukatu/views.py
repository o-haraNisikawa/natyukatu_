from datetime import datetime
import os
import numpy as np
from pathlib import Path
from apps.app import db
from apps.crud.models import User
from flask import Blueprint,render_template,current_app,send_from_directory
import pandas as pd
import joblib
from sqlalchemy import desc
from sklearn.feature_extraction.text import CountVectorizer
 
from flask import(
    Blueprint,
    current_app,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
    flash,
    abort,
)
 
from apps.natyukatu.models import (
    Recruitment,
    Like,
    Participants,
    ViewHistory,
    RecruitmentTag,
    Entry,
    ActiveMessage,
    ThanksPoint,
    ContactHistory,
    ParticipationHistory,
    RecruitmentHistory,
)
 
from apps.natyukatu.forms import (
    ParticipationForm,
    RecruitmentForm,
    ContactForm,
    LikeForm,
    MessageForm,
    RecruitmentDeleteForm,
    RecruitmentUpdateForm,
    HistoryUpdateForm,
    SearchForm,
    ApplicantDecisionForm,
    WithdrawalForm,
    UserUpdateForm,
 
)
 
from flask_login import current_user,login_required
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError
 
from apps.crud.models import User
 
dt = Blueprint("natyukatu",
                __name__,
                template_folder="templates",
                static_folder="static",)
 
#ユーザーIDを取得
def get_user_id():
    return current_user.user_id
 
#募集情報を取得
def get_recruitment(recruitment_id):
    recruitment = Recruitment.query.filter_by(
        id=recruitment_id
    ).first()
 
    if recruitment is None:
        abort(404)
 
    return recruitment
 
#トップ画面表示
@dt.route("/top", methods=["GET", "POST"])
def top():

#各メソッドを持ってくる
    #ユーザーID取得
    user_id = get_user_id()

    #検索フォーム(prefixを使っているので複数のformsを区別してる)
    search_form = SearchForm(prefix="search")
    #タグ検索用
    set_tag_choices(search_form)

    #お気に入りフォーム
    like_form = LikeForm(prefix="like")

    # POSTリクエスト時の処理
    if request.method == "POST":

        #お気に入りボタンが押された場合
        if "like-submit" in request.form and like_form.validate_on_submit():
            recruitment_id = int(like_form.recruitment_id.data)
            
            existing_like = Like.query.filter_by(
                user_id=user_id, 
                recruitment_id=recruitment_id
            ).first()
            
            if existing_like:
                delete_like(user_id, recruitment_id)
            else:
                add_like(user_id, recruitment_id)
                
            return redirect(url_for("dt.top"))

    #入力されたタグIDを取得
    selected_tag_id = search_form.tag_id.data
    #入力された検索ワード取得
    keyword = search_form.keyword.data if hasattr(search_form, 'keyword') else None
    # 絞り込み条件を反映した募集一覧を取得
    recruitments = get_recruitment_list(keyword=keyword,tag_id=selected_tag_id)
    #お気に入り一覧取得
    like_list = get_like_list(user_id)
    #閲覧履歴取得
    view_history_list = get_view_history_list(user_id)

    return render_template(
        "natyukatu/top.html",
        form=search_form,
        like_form=like_form,
        recruitments=recruitments,
        like_list=like_list,
        view_history_list=view_history_list,
        )
 
# 募集一覧取得（タグとワードで絞り込み有）
def get_recruitment_list(keyword=None, tag_id=None):
    query = db.session.query(Recruitment)
    
    # キーワード検索がある場合
    if keyword:
        query = query.filter(Recruitment.title.like(f"%{keyword}%"))
        
    # タグIDが指定されており、「すべて」（0やNoneなど）ではない場合
    if tag_id and tag_id != 0:
        query = query.filter(Recruitment.tag_id == tag_id)
        
    recruitments = query.order_by(desc(Recruitment.created_at)).all()
    return recruitments

#タグ取得
def set_tag_choices(form):
    form.tag_id.choices = [(0, "すべて")] + [
        (tag.tag_id, tag.tag_name) 
        for tag in RecruitmentTag.query.all()
    ]

# お気に入り一覧取得
def get_like_list(user_id):
    query = (
        db.session.query(Recruitment)
        .join(Like, Recruitment.id == Like.recruitment_id)  # Likeテーブルと結合
        .filter(Like.user_id == user_id)  # ログイン中のユーザーIDで絞り込み
        .order_by(desc(Recruitment.created_at))
    )
    recruitments = query.all()
    return recruitments
 
#閲覧履歴一覧取得
def get_view_history_list(user_id):
    query = (
        db.session.query(Recruitment)
        .join(ViewHistory, Recruitment.id == ViewHistory.recruitment_id)  
        .filter(ViewHistory.user_id == user_id)  # ログイン中のユーザーIDで絞り込み
        .order_by(desc(Recruitment.added_at))
    )
    recruitments = query.all()
    return recruitments

#お気に入り登録
def add_like(user_id,recruitment_id):
    recruitment = get_recruitment(recruitment_id)
 
    like = Like.query.filter_by(
        user_id=user_id,
        recruitment_id=recruitment_id
    ).first()
 
    if like is None:
        like = Like(
            user_id=user_id,
            recruitment_id=recruitment_id
        )
        db.session.add(like)
        db.session.commit()
 
#お気に入り解除
def delete_like(user_id,recruitment_id):

    like = Like.query.filter_by(
        user_id=user_id,
        recruitment_id=recruitment_id
    ).first()

    #データが存在していれば削除してコミット
    if like is not None:
        db.session.delete(like)
        db.session.commit()
 
#募集詳細
def activity_detail(active_id):
    recruitment = get_recruitment(active_id)
 
    if current_user.is_authenticated:
        history = ViewHistory(
            id=None,
            active_id=active_id,
            user_id=get_user_id(),
            apdate_at=datetime.now()
        )
 
        db.session.add(history)
        db.session.commit()
 
    return render_template(
        "natyukatu/recruitment_detail.html",
        recruitment=recruitment
    )

#ユーザー詳細

#参加履歴・募集履歴取得

@dt.route("/participations")
@login_required
def participations():
    histories = ParticipationHistory.query.filter_by(
        user_id=get_user_id()
    ).all()
 
    return render_template(
        "natyukatu/participations.html",
        histories=histories
    )
 
 
@dt.route("/recruitments")
@login_required
def recruitments():
    histories = RecruitmentHistory.query.filter_by(
        user_id=get_user_id()
    ).all()
 
    return render_template(
        "natyukatu/recruitments.html",
        histories=histories
    )
 
 
# =====================================
# ⑧ 新規募集登録
# =====================================
 
@dt.route("/recruitments/new", methods=["GET", "POST"])
@login_required
def create_recruitment():
    form = RecruitmentForm()
 
    form.tag_id.choices = [
        (tag.tag_id, tag.tag_name)
        for tag in RecruitmentTag.query.all()
    ]
 
    if form.validate_on_submit():
        recruitment = Recruitment(
            active_id=make_id(),
            user_id=get_user_id(),
            title=form.title.data,
            description=form.description.data,
            photo=form.photo.data.read(),
            tag_id=form.tag_id.data,
            location_prefecture=form.location_prefecture.data,
            location_city=form.location_city.data,
            location_detail=form.location_detail.data,
            start_at=form.start_at.data,
            end_at=form.end_at.data,
            application_start_at=form.application_start_at.data,
            application_end_at=form.application_end_at.data,
            capacity=form.capacity.data,
            eligibility=form.eligibility.data,
            required_items=form.required_items.data,
            status="募集中",
            review_status="未確認"
        )
 
        db.session.add(recruitment)
        db.session.commit()
 
        flash("募集を登録しました")
 
        return redirect(url_for("natyukatu.recruitments"))
 
    return render_template(
        "natyukatu/create_recruitment.html",
        form=form
    )
 
 
# =====================================
# ⑨ 募集情報更新
# =====================================
 
@dt.route(
    "/recruitments/<active_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_recruitment(active_id):
    recruitment = get_recruitment(active_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    form = RecruitmentUpdateForm()
 
    form.tag_id.choices = [
        (tag.tag_id, tag.tag_name)
        for tag in RecruitmentTag.query.all()
    ]
 
    if form.validate_on_submit():
        recruitment.title = form.title.data
        recruitment.description = form.description.data
 
        if form.photo.data:
            recruitment.photo = form.photo.data.read()
 
        recruitment.tag_id = form.tag_id.data
        recruitment.location_prefecture = form.location_prefecture.data
        recruitment.location_city = form.location_city.data
        recruitment.location_detail = form.location_detail.data
        recruitment.start_at = form.start_at.data
        recruitment.end_at = form.end_at.data
        recruitment.application_start_at = form.application_start_at.data
        recruitment.application_end_at = form.application_end_at.data
        recruitment.capacity = form.capacity.data
        recruitment.eligibility = form.eligibility.data
        recruitment.required_items = form.required_items.data
 
        db.session.commit()
 
        flash("募集情報を更新しました")
 
        return redirect(url_for("natyukatu.recruitments"))
 
    elif request.method == "GET":
        form.title.data = recruitment.title
        form.description.data = recruitment.description
        form.tag_id.data = recruitment.tag_id
        form.location_prefecture.data = recruitment.location_prefecture
        form.location_city.data = recruitment.location_city
        form.location_detail.data = recruitment.location_detail
        form.start_at.data = recruitment.start_at
        form.end_at.data = recruitment.end_at
        form.application_start_at.data = recruitment.application_start_at
        form.application_end_at.data = recruitment.application_end_at
        form.capacity.data = recruitment.capacity
        form.eligibility.data = recruitment.eligibility
        form.required_items.data = recruitment.required_items
 
    return render_template(
        "natyukatu/edit_recruitment.html",
        form=form,
        recruitment=recruitment
    )
 
 
# =====================================
# ⑩ 募集削除
# =====================================
 
@dt.route(
    "/recruitments/<active_id>/delete",
    methods=["POST"]
)
@login_required
def delete_recruitment(active_id):
    recruitment = get_recruitment(active_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    db.session.delete(recruitment)
    db.session.commit()
 
    flash("募集を削除しました")
 
    return redirect(url_for("natyukatu.recruitments"))
 
 
# =====================================
# ⑪ 参加申し込み
# =====================================
 
@dt.route(
    "/activities/<active_id>/apply",
    methods=["GET", "POST"]
)
@login_required
def apply_activity(active_id):
    recruitment = get_recruitment(active_id)
    form = ParticipationForm()
 
    if form.validate_on_submit():
 
        if recruitment.application_end_at < datetime.now():
            flash("募集期間が終了しています")
            return redirect(url_for(
                "natyukatu.activity_detail",
                active_id=active_id
            ))
 
        entry = Entry(
            applicant_id=make_id(),
            activity_id=active_id,
            user_id=get_user_id(),
            particpant_count=form.participant_count.data,
            message=form.message.data,
            status="申込中",
            cansel_at=datetime.now()
        )
 
        db.session.add(entry)
        db.session.commit()
 
        flash("参加申し込みが完了しました")
 
        return redirect(url_for("natyukatu.apply_complete"))
 
    return render_template(
        "natyukatu/apply.html",
        form=form,
        recruitment=recruitment
    )
 
 
# =====================================
# ⑫ 申込完了画面
# =====================================
 
@dt.route("/apply/complete")
@login_required
def apply_complete():
    return render_template("natyukatu/apply_complete.html")
 
 
# =====================================
# ⑬ 申込者一覧取得
# =====================================
 
@dt.route(
    "/recruitments/<active_id>/applicants"
)
@login_required
def applicants(active_id):
    recruitment = get_recruitment(active_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    entries = Entry.query.filter_by(
        activity_id=active_id
    ).all()
 
    return render_template(
        "natyukatu/applicants.html",
        entries=entries,
        recruitment=recruitment
    )
 
 
# =====================================
# ⑭ 申込状態変更（可・否）
# =====================================
 
@dt.route(
    "/applicants/<applicant_id>/decision",
    methods=["POST"]
)
@login_required
def applicant_decision(applicant_id):
    entry = Entry.query.filter_by(
        applicant_id=applicant_id
    ).first_or_404()
 
    recruitment = get_recruitment(entry.activity_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    form = ApplicantDecisionForm()
 
    if form.validate_on_submit():
        entry.status = form.status.data
        entry.update_at = datetime.now()
 
        db.session.commit()
 
        flash("申込状態を変更しました")
 
    return redirect(url_for(
        "natyukatu.applicants",
        active_id=entry.activity_id
    ))
 
 
# =====================================
# ⑮ 申込者を一覧から削除
# =====================================
 
@dt.route(
    "/applicants/<applicant_id>/delete",
    methods=["POST"]
)
@login_required
def delete_applicant(applicant_id):
    entry = Entry.query.filter_by(
        applicant_id=applicant_id
    ).first_or_404()
 
    recruitment = get_recruitment(entry.activity_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    db.session.delete(entry)
    db.session.commit()
 
    flash("申込者を削除しました")
 
    return redirect(url_for(
        "natyukatu.applicants",
        active_id=recruitment.active_id
    ))
 
 
# =====================================
# ⑯ 活動用メッセージ投稿
# =====================================
 
@dt.route(
    "/messages/<active_id>",
    methods=["GET", "POST"]
)
@login_required
def messages(active_id):
    recruitment = get_recruitment(active_id)
    form = MessageForm()
 
    if form.validate_on_submit():
        message = ActiveMessage(
            user_id=get_user_id(),
            message=form.message.data,
            nickname=current_user.nickname,
            created_at=datetime.now(),
            post_at=datetime.now(),
            update_at=datetime.now()
        )
 
        db.session.add(message)
        db.session.commit()
 
        flash("メッセージを投稿しました")
 
        return redirect(url_for(
            "natyukatu.messages",
            active_id=active_id
        ))
 
    return render_template(
        "natyukatu/messages.html",
        form=form,
        recruitment=recruitment
    )
 
 
# =====================================
# ⑰ お問い合わせ
# =====================================
 
@dt.route(
    "/contact",
    methods=["GET", "POST"]
)
@login_required
def contact():
    form = ContactForm()
 
    if form.validate_on_submit():
        contact_history = ContactHistory(
            contact_id=make_id(),
            user_id=get_user_id(),
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            body=form.body.data
        )
 
        db.session.add(contact_history)
        db.session.commit()
 
        flash("お問い合わせを送信しました")
 
        return redirect(url_for("natyukatu.index"))
 
    return render_template(
        "natyukatu/contact.html",
        form=form
    )
 
 
# =====================================
# ⑱ サンクスボタン
# =====================================
 
@dt.route(
    "/thanks/<active_id>/<user_id>",
    methods=["POST"]
)
@login_required
def thanks(active_id, user_id):
    recruitment = get_recruitment(active_id)
 
    if recruitment.user_id != get_user_id():
        abort(403)
 
    point = ThanksPoint(
        point_id=make_id(),
        user_id=user_id,
        activity_id=active_id,
        record_id=make_id(),
        point_count=1
    )
 
    db.session.add(point)
    db.session.commit()
 
    flash("サンクスポイントを送りました")
 
    return redirect(url_for(
        "natyukatu.participations"
    ))
 
 
# =====================================
# ⑲ ランキング生成
# =====================================
 
@dt.route("/ranking")
def ranking():
    results = db.session.query(
        ThanksPoint.user_id,
        db.func.sum(ThanksPoint.point_count).label("total_points")
    ).group_by(
        ThanksPoint.user_id
    ).order_by(
        db.func.sum(ThanksPoint.point_count).desc()
    ).all()
 
    return render_template(
        "natyukatu/ranking.html",
        rankings=results
    )
 
 
# =====================================
# ⑳ ユーザー情報変更
# =====================================
 
@dt.route(
    "/mypage/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():
    form = UserUpdateForm()
 
    user = User.query.filter_by(
        user_id=get_user_id()
    ).first_or_404()
 
    if form.validate_on_submit():
        user.username = form.username.data
        user.nickname = form.nickname.data
        user.age = form.age.data
        user.email = form.email.data
        user.emergency_contact = form.emergency_contact.data
 
        db.session.commit()
 
        flash("ユーザー情報を変更しました")
 
        return redirect(url_for("natyukatu.mypage"))
 
    elif request.method == "GET":
        form.username.data = user.username
        form.nickname.data = user.nickname
        form.age.data = user.age
        form.email.data = user.email
        form.emergency_contact.data = user.emergency_contact
 
    return render_template(
        "natyukatu/edit_profile.html",
        form=form
    )
 
 
# =====================================
# ㉑ ユーザー退会
# =====================================
 
@dt.route(
    "/mypage/withdrawal",
    methods=["GET", "POST"]
)
@login_required
def withdrawal():
    form = WithdrawalForm()
 
 
    if form.validate_on_submit():
        user = User.query.filter_by(
            user_id=get_user_id()
        ).first_or_404()
 
        if not user.check_password(form.password.data):
            flash("パスワードが違います")
            return render_template(
                "natyukatu/withdrawal.html",
                form=form
            )
 
        db.session.delete(user)
        db.session.commit()
 
        from flask_login import logout_user
        logout_user()
 
        flash("退会しました")
 
        return redirect(url_for("natyukatu.index"))
 
    return render_template(
        "natyukatu/withdrawal.html",
        form=form
    )
 
 
# =====================================
# ㉒ 管理者用削除
# =====================================
 
@dt.route(
    "/admin/recruitments/<active_id>/delete",
    methods=["POST"]
)
@login_required
def admin_delete_recruitment(active_id):
    # 管理者権限の確認をここに追加する
    recruitment = get_recruitment(active_id)
 
    db.session.delete(recruitment)
    db.session.commit()
 
    flash("募集を削除しました")
 
    return redirect(url_for("natyukatu.admin"))
 
 
@dt.route("/admin")
@login_required
def admin():
    recruitments = Recuruitment.query.all()
    entries = Entry.query.all()
    users = User.query.all()
 
    return render_template(
        "natyukatu/admin.html",
        recruitments=recruitments,
        entries=entries,
        users=users
    )
 
 