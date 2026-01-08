from flask import Blueprint, render_template, request, redirect, url_for
from models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """トップページ - ユーザー作成と一覧"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            User.create(name=name)
        return redirect(url_for("main.index"))

    # 全ユーザーを取得
    users = User.select().order_by(User.id.desc())
    return render_template("index.html", users=users)

@main_bp.route("/ranking")
def ranking():
    """ランキングページ - コイン数でソート"""
    # コイン数の多い順にユーザーを取得
    users = User.select().order_by(User.coin.desc())
    return render_template("ranking.html", users=users)
