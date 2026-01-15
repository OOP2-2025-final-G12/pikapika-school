from flask import Blueprint, render_template, request, redirect, url_for, session
from peewee import DoesNotExist
from models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            # 既存 or 新規ユーザー取得
            user, created = User.get_or_create(name=name)

            # user_id を session に保存
            session["user_id"] = user.id

            return redirect(url_for("main.select"))

    # セッションからユーザーを取得
    user = None
    user_id = session.get("user_id")
    if user_id:
        try:
            user = User.get_by_id(user_id)
        except DoesNotExist:
            session.clear()

    return render_template("index.html", user=user)


@main_bp.route("/select")
def select():
    user_id = session.get("user_id")

    # user_id がない場合はトップへ
    if not user_id:
        return redirect(url_for("main.index"))

    # 現在のユーザーを取得
    try:
        user = User.get_by_id(user_id)
    except DoesNotExist:
        session.clear()
        return redirect(url_for("main.index"))

    # 全ユーザーを取得
    users = User.select().order_by(User.id.desc())
    return render_template("select.html", user=user, users=users)


@main_bp.route("/ranking")
def ranking():
    """ランキングページ - コイン数でソート"""
    # コイン数の多い順にユーザーを取得
    users = User.select().order_by(User.coin.desc())
    return render_template("ranking.html", users=users)
