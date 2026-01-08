from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
import random
from models import User

class2_bp = Blueprint('class2', __name__, url_prefix='/class2', template_folder='../templates')

def _get_user_and_cookie():
    """class1.py と同一のユーザー取得ロジック"""
    user_id = session.get("user_id")
    if user_id:
        user = User.get_by_id(user_id)
        if user:
            return user, None

    cookie_val = request.cookies.get("ppk_user")
    if cookie_val:
        try:
            cookie_uid = int(cookie_val)
        except (TypeError, ValueError):
            cookie_uid = None
        if cookie_uid:
            user = User.get_or_none(User.id == cookie_uid)
            if user:
                session["user_id"] = user.id
                return user, None

    user = User.get_or_none(User.id == 1)
    if not user:
        user = User.create(name="テストユーザー")

    return user, str(user.id)

@class2_bp.route('/')
def class2():
    user, cookie_to_set = _get_user_and_cookie()
    resp = make_response(render_template('class2.html', user=user))
    if cookie_to_set:
        resp.set_cookie("ppk_user", cookie_to_set, max_age=60*60*24*30)
    return resp

# 共通の処理を関数化してコードをすっきりさせる
def handle_level(quiz_variations, level_num):
    user, cookie_to_set = _get_user_and_cookie()

    if request.method == 'POST':
        chosen_idx = session.get(f'class2_level{level_num}_chosen', 0)
        chosen = quiz_variations[chosen_idx]
        correct_answers = chosen['answers']

        score = 0
        for q, ans in correct_answers.items():
            if request.form.get(q) == ans:
                score += 1

        ticket_rewards = {1: 1, 2: 2, 3: 4}
        ticket_award = ticket_rewards.get(level_num, 1)

        if score >= 8:
            user.ticket += ticket_award
            user.save()
            flash(f'素晴らしい！ {score}問正解で ticket を{ticket_award}枚獲得！（現在 {user.ticket}枚）', 'success')
        else:
            flash(f'{score}問正解でした。8問以上正解で ticket が{ticket_award}枚もらえます！', 'info')

        # セッションに結果を一時保存してリダイレクト
        session['quiz_result'] = {
            'score': score,
            'total': 10,
            'level': level_num,
            'passed': score >= 8,
            'ticket_award': ticket_award if score >= 8 else 0
        }

        resp = make_response(redirect(url_for('class2.result')))
    else:
        # GET: 新しい問題を選択
        chosen = random.choice(quiz_variations)
        idx = quiz_variations.index(chosen)
        session[f'class2_level{level_num}_chosen'] = idx
        session.pop('quiz_result', None)  # 前の結果をクリア

        resp = make_response(render_template(chosen['template'], user=user))

    if cookie_to_set:
        resp.set_cookie("ppk_user", cookie_to_set, max_age=60*60*24*30)
    return resp

@class2_bp.route('/level1', methods=['GET', 'POST'])
def level1():
    quiz_variations = [
        {
            'template': 'level1_1.html',
            'answers': {'q1': 'D', 'q2': 'B', 'q3': 'D', 'q4': 'C', 'q5': 'B',
                        'q6': 'B', 'q7': 'D', 'q8': 'A', 'q9': 'C', 'q10': 'B'}
        }
        # 追加バリエーションがあればここに
    ]
    return handle_level(quiz_variations, 1)

@class2_bp.route('/level2', methods=['GET', 'POST'])
def level2():
    quiz_variations = [
        {
            'template': 'level2_1.html',
            'answers': {'q1': 'C', 'q2': 'C', 'q3': 'B', 'q4': 'D', 'q5': 'C',
                        'q6': 'C', 'q7': 'A', 'q8': 'D', 'q9': 'B', 'q10': 'A'}
        }
        # 追加バリエーションがあればここに
    ]
    return handle_level(quiz_variations, 2)

@class2_bp.route('/level3', methods=['GET', 'POST'])
def level3():
    quiz_variations = [
        {
            'template': 'level3_1.html',
            'answers': {'q1': 'D', 'q2': 'D', 'q3': 'A', 'q4': 'D', 'q5': 'B',
                        'q6': 'B', 'q7': 'D', 'q8': 'C', 'q9': 'E', 'q10': 'D'}
        }
        # 追加バリエーションがあればここに
    ]
    return handle_level(quiz_variations, 3)

@class2_bp.route('/result')
def result():
    user, cookie_to_set = _get_user_and_cookie()
    result_data = session.pop('quiz_result', None)

    if not result_data:
        flash('不正なアクセスです。', 'error')
        return redirect(url_for('class2.class2'))

    resp = make_response(render_template(
        'level_result.html',
        score=result_data['score'],
        total=result_data['total'],
        passed=result_data['passed'],
        ticket_award=result_data['ticket_award'],
        user=user
    ))
    if cookie_to_set:
        resp.set_cookie("ppk_user", cookie_to_set, max_age=60*60*24*30)
    return resp