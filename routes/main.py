from flask import Blueprint, render_template, request, redirect, url_for, session
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

    return render_template("index.html")


@main_bp.route("/select")
def select():
    user_id = session.get("user_id")

    # user_id がない場合はトップへ
    if not user_id:
        return redirect(url_for("main.index"))

    user = User.get_by_id(user_id)

    return render_template("select.html", user=user)
