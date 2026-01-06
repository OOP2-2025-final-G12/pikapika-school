from flask import Blueprint, render_template, request, redirect, url_for
from models import User

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """トップページ"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            User.create(name=name)

        # ★ そのまま /select へ
        return redirect(url_for("main.select"))

    return render_template("index.html")


@main_bp.route("/select")
def select():
    """セレクト画面"""
    # ★ 最新のユーザーを1人取得
    user = User.select().order_by(User.id.desc()).first()

    if not user:
        return redirect(url_for("main.index"))

    return render_template("select.html", user=user)


@main_bp.route("/class1")
def class1():
    return "<h1>授業①（準備中）</h1>"


@main_bp.route("/class2")
def class2():
    return "<h1>授業②（準備中）</h1>"

