from flask import Blueprint, render_template, request, session, make_response, jsonify
from peewee import DoesNotExist
from models import User

game_bp = Blueprint("game", __name__)


def _get_user_and_cookie():
    """Retrieve logged-in user using session or cookie. If none, create a test user and
    request that the caller set a cookie with that user's id.

    Returns: (user, cookie_value_or_None)
    - user: models.user.User instance
    - cookie_value_or_None: if non-None, caller should set a cookie 'ppk_user' to this value
    """
    # 1) session にユーザーがあれば優先
    user_id = session.get("user_id")
    if user_id:
        try:
            user = User.get_by_id(user_id)
            if user:
                return user, None
        except DoesNotExist:
            pass

    # 2) cookie に保存されたユーザーID があればそれを使う
    cookie_val = request.cookies.get("ppk_user")
    if cookie_val:
        try:
            cookie_uid = int(cookie_val)
            user = User.get_or_none(User.id == cookie_uid)
            if user:
                # セッションにも設定しておく
                session["user_id"] = user.id
                return user, None
        except (TypeError, ValueError):
            pass

    # 3) 上記が無ければテスト用ユーザーを作成（既に id=1 のユーザーがあればそれを使う）
    user = User.get_or_none(User.id == 1)
    if not user:
        user = User.create(name="テストユーザー")

    # 呼び出し元に cookie をセットするよう指示（ユーザーID を保存）
    return user, str(user.id)


@game_bp.route("/game")
def game():
    """ゲームページ - ルーレットゲーム"""
    user, cookie_to_set = _get_user_and_cookie()
    users = User.select().order_by(User.coin.desc())
    resp = make_response(render_template("game.html", user=user, users=users))
    if cookie_to_set:
        resp.set_cookie("ppk_user", cookie_to_set, max_age=60 * 60 * 24 * 30)  # 30日
    return resp


@game_bp.route("/game/spin", methods=["POST"])
def game_spin():
    """ルーレットを回してチケット消費・コイン付与"""
    user, _ = _get_user_and_cookie()

    if not user:
        return jsonify({"success": False, "message": "ユーザーが見つかりません"}), 400

    # チケットが足りるかチェック
    if user.ticket < 1:
        return jsonify({"success": False, "message": "チケットが足りません"}), 400

    # リクエストから獲得コイン数を取得
    data = request.get_json()
    coins = data.get("coins", 0)

    # チケット消費とコイン付与
    user.ticket -= 1
    user.coin += coins
    user.save()

    return jsonify(
        {
            "success": True,
            "coins": coins,
            "newTicketCount": user.ticket,
            "newCoinCount": user.coin,
        }
    )
