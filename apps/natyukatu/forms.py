from flask_wtf.form import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields import (
    StringField,
    PasswordField,
    TextAreaField,
    SelectField,
    IntegerField,
    DateTimeLocalField,
    FileField,
    HiddenField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
    EqualTo,
)

class SearchForm(FlaskForm):
    # キーワード検索欄
    keyword = StringField(
        validators=[
            Optional(),
            Length(max=50)
        ]
    )
    # タグ選択欄
    tag_id = SelectField(
        choices=[],
        coerce=int
    )
    submit = SubmitField("検索する")


#お気に入り
class LikeForm(FlaskForm):
    recruitment_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField("お気に入り登録/解除")


# =====================================
# ① 参加申し込みフォーム
# =====================================

class ParticipationForm(FlaskForm):
    participant_count = IntegerField(
        "参加人数",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    message = TextAreaField(
        "応募メッセージ",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    submit = SubmitField("参加申し込み")


# =====================================
# ② 新規募集登録フォーム
# =====================================

class RecruitmentForm(FlaskForm):
    title = StringField(
        "募集タイトル",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    description = TextAreaField(
        "募集内容",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    photo = FileField(
        "募集画像",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "画像を選択してください")
        ]
    )

    tag_id = SelectField(
        "活動タグ",
        choices=[],
        validators=[DataRequired()]
    )

    location_prefecture = StringField(
        "都道府県",
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )

    location_city = StringField(
        "市区町村",
        validators=[
            DataRequired(),
            Length(max=10)
        ]
    )

    location_detail = StringField(
        "詳しい住所",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    start_at = DateTimeLocalField(
        "活動開始日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    end_at = DateTimeLocalField(
        "活動終了日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    application_start_at = DateTimeLocalField(
        "募集開始日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    application_end_at = DateTimeLocalField(
        "募集終了日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    capacity = IntegerField(
        "募集人数",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    eligibility = StringField(
        "参加条件",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    required_items = StringField(
        "持ち物",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    submit = SubmitField("募集を登録")


# =====================================
# ③ お問い合わせフォーム
# =====================================

class ContactForm(FlaskForm):
    name = StringField(
        "名前",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(),
            Email(),
            Length(max=30)
        ]
    )

    subject = StringField(
        "お問い合わせ件名",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    body = TextAreaField(
        "お問い合わせ内容",
        validators=[DataRequired()]
    )

    submit = SubmitField("送信する")





# =====================================
# ⑤ メッセージフォーム
# =====================================

class MessageForm(FlaskForm):
    message = StringField(
        "メッセージ",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    submit = SubmitField("投稿する")


# =====================================
# ⑥ 募集削除フォーム
# =====================================

class RecruitmentDeleteForm(FlaskForm):
    active_id = HiddenField(
        "募集ID",
        validators=[DataRequired()]
    )

    confirm = BooleanField(
        "この募集を削除することに同意します",
        validators=[DataRequired()]
    )

    submit = SubmitField("募集を削除")


# =====================================
# ⑦ 募集更新フォーム
# =====================================

class RecruitmentUpdateForm(FlaskForm):
    title = StringField(
        "募集タイトル",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    description = TextAreaField(
        "募集内容",
        validators=[
            DataRequired(),
            Length(max=50)
        ]
    )

    photo = FileField(
        "募集画像",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png"])
        ]
    )

    tag_id = SelectField(
        "活動タグ",
        choices=[],
        validators=[DataRequired()]
    )

    location_prefecture = StringField(
        "都道府県",
        validators=[
            DataRequired(),
            Length(max=5)
        ]
    )

    location_city = StringField(
        "市区町村",
        validators=[
            DataRequired(),
            Length(max=10)
        ]
    )

    location_detail = StringField(
        "詳しい住所",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    start_at = DateTimeLocalField(
        "活動開始日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    end_at = DateTimeLocalField(
        "活動終了日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    application_start_at = DateTimeLocalField(
        "募集開始日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    application_end_at = DateTimeLocalField(
        "募集終了日時",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    capacity = IntegerField(
        "募集人数",
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    eligibility = StringField(
        "参加条件",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    required_items = StringField(
        "持ち物",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    submit = SubmitField("変更を保存")


# =====================================
# ⑧ 参加・募集履歴更新フォーム(分ける)
# =====================================

class HistoryUpdateForm(FlaskForm):
    status = SelectField(
        "履歴状態",
        choices=[
            ("募集中", "募集中"),
            ("受付終了", "受付終了"),
            ("参加予定", "参加予定"),
            ("参加済み", "参加済み"),
            ("キャンセル", "キャンセル")
        ],
        validators=[DataRequired()]
    )

    review_status = SelectField(
        "確認状態",
        choices=[
            ("未確認", "未確認"),
            ("確認済み", "確認済み")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("履歴を更新")




# =====================================
# ⑩ 申込者一覧・可否ボタンフォーム
# =====================================

class ApplicantDecisionForm(FlaskForm):
    applicant_id = HiddenField(
        "申込者ID",
        validators=[DataRequired()]
    )

    status = SelectField(
        "申込可否",
        choices=[
            ("可", "可"),
            ("否", "否")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("決定する")


# =====================================
# ⑪ ユーザー退会フォーム
# =====================================

class WithdrawalForm(FlaskForm):
    password = PasswordField(
        "パスワード",
        validators=[DataRequired()]
    )

    confirm = BooleanField(
        "退会することに同意します",
        validators=[DataRequired()]
    )

    submit = SubmitField("退会する")


# =====================================
# ⑫ ユーザー情報更新フォーム
# =====================================

class UserUpdateForm(FlaskForm):
    username = StringField(
        "名前",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    nickname = StringField(
        "ニックネーム",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    age = IntegerField(
        "年齢",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=120)
        ]
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone_number = StringField(
        "電話番号",
        validators=[
            Optional(),
            Length(max=30)
        ]
    )

    submit = SubmitField("変更を保存")
