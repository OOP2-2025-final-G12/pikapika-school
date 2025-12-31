from flask import Blueprint, render_template, redirect, url_for, session, request
import random
from models.user import User

game_bp = Blueprint("game", __name__)

@game_bp.route("/game")
def game():
    # ログインチェック
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))

    user = User.get_by_id(user_id)
    return render_template("game.html", user=user)

@game_bp.route("/game/play", methods=["POST"])
def play():
    user = User.get_by_id(session.get("user_id"))

    if user.ticket <= 0:
        return redirect(url_for("game.game"))

    # チケット消費
    user.ticket -= 1

    # ルーレット結果（0〜10）
    reward = random.choice([0, 1, 2, 3, 5, 10])
    user.coin += reward
    user.save()

    return render_template("game_result.html", user=user, reward=reward)
