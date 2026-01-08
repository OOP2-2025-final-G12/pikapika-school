# ...existing code...
from flask import Blueprint, render_template, redirect, url_for, session, request
import random
from models.user import User

class1_bp = Blueprint("class1", __name__)

# 問題プール（例：各レベル12問程度。必要に応じて追加してください）
QUESTIONS = {
    1: [
        {"id": 1, "q": "りんごが3個あります。さらに2個買うと合計はいくつ？", "choices": ["4", "5", "6", "3"], "answer": 1},
        {"id": 2, "q": "5 - 2 = ?", "choices": ["1", "2", "3", "4"], "answer": 2},
        {"id": 3, "q": "1メートルは何センチ？", "choices": ["10cm", "100cm", "1000cm", "1cm"], "answer": 1},
        {"id": 4, "q": "3 + 4 = ?", "choices": ["6", "7", "8", "9"], "answer": 1},
        {"id": 5, "q": "2 × 3 = ?", "choices": ["5", "6", "7", "8"], "answer": 1},
        {"id": 6, "q": "10 ÷ 2 = ?", "choices": ["2", "3", "4", "5"], "answer": 3},
        {"id": 7, "q": "1週間は何日？", "choices": ["5", "6", "7", "8"], "answer": 2},
        {"id": 8, "q": "三角形の角の合計は何度？", "choices": ["90度", "180度", "270度", "360度"], "answer": 1},
        {"id": 9, "q": "10より小さい偶数はどれ？", "choices": ["3", "4", "7", "9"], "answer": 1},
        {"id":10, "q": "午前の次は？", "choices": ["午後", "夜", "朝", "深夜"], "answer": 0},
        {"id":11, "q": "4個のりんごを2人で均等に分けると1人あたり何個？", "choices": ["1個", "2個", "3個", "4個"], "answer": 1},
        {"id":12, "q": "5 + 5 = ?", "choices": ["9", "10", "11", "12"], "answer": 1},
    ],
    2: [
        {"id": 1, "q": "12 ÷ 3 = ?", "choices": ["3", "4", "5", "6"], "answer": 1},
        {"id": 2, "q": "6 × 7 = ?", "choices": ["42", "36", "48", "40"], "answer": 0},
        {"id": 3, "q": "100cm = ? m", "choices": ["0.1m", "1m", "10m", "100m"], "answer": 1},
        {"id": 4, "q": "平方の記号は？", "choices": ["³", "²", "√", "％"], "answer": 1},
        {"id": 5, "q": "45分は何時間？", "choices": ["0.45時間", "0.75時間", "1時間", "0.50時間"], "answer": 1},
        {"id": 6, "q": "5/10 を簡単にすると？", "choices": ["1/2", "1/5", "2/5", "5/2"], "answer": 0},
        {"id": 7, "q": "角度が直角なのは何度？", "choices": ["45度", "90度", "180度", "360度"], "answer": 1},
        {"id": 8, "q": "1000メートルは何キロ？", "choices": ["0.1km", "1km", "10km", "100km"], "answer": 1},
        {"id": 9, "q": "素数はどれ？", "choices": ["4", "6", "7", "9"], "answer": 2},
        {"id":10, "q": "図形の面積を求める公式は？", "choices": ["演算ごとに異なる", "常に同じ", "存在しない", "面積は計測できない"], "answer": 0},
        {"id":11, "q": "3^2 = ?", "choices": ["6", "9", "8", "3"], "answer": 1},
        {"id":12, "q": "分数の足し算 1/4 + 1/4 = ?", "choices": ["1/2", "1/4", "1", "3/4"], "answer": 0},
    ],
    3: [
        {"id": 1, "q": "水の化学式はどれ？", "choices": ["H2O", "CO2", "O2", "NaCl"], "answer": 0},
        {"id": 2, "q": "酸素の元素記号はどれ？", "choices": ["Ox", "O", "Os", "Op"], "answer": 1},
        {"id": 3, "q": "炭酸水素ナトリウム（重曹）の化学式は？", "choices": ["Na2CO3", "NaHCO3", "KCl", "NH3"], "answer": 1},
        {"id": 4, "q": "メタン CH4 の燃焼反応 CH4 + ? O2 → CO2 + 2 H2O における O2 の係数は？", "choices": ["1", "2", "3", "4"], "answer": 1},
        {"id": 5, "q": "2x + 3 = 11 のとき、x は？", "choices": ["3", "4", "5", "6"], "answer": 1},
        {"id": 6, "q": "方程式 x^2 - 4 = 0 の実数解の一つは？", "choices": ["-2", "0", "2", "4"], "answer": 2},
        {"id": 7, "q": "直角三角形で2辺の長さが 3 と 4 のとき、斜辺の長さは？", "choices": ["5", "6", "7", "√13"], "answer": 0},
        {"id": 8, "q": "密度 = 質量 / 体積。質量 200 g、体積 50 cm³ の密度は？", "choices": ["0.25 g/cm³", "2 g/cm³", "4 g/cm³", "10000 g/cm³"], "answer": 2},
        {"id": 9, "q": "関数 y = 2x + 1 において x = 3 のとき y の値は？", "choices": ["5", "6", "7", "8"], "answer": 2},
        {"id":10, "q": "二次方程式の判別式 Δ = b^2 - 4ac が負のとき、解の種類は？", "choices": ["実数の異なる2解", "重解（重複解）", "虚数解（実数解なし）", "解なし"], "answer": 2},
        {"id":11, "q": "ある数の3乗が 27 のとき、その数は？", "choices": ["2", "3", "9", "-3"], "answer": 1},
        {"id":12, "q": "3(x - 2) = 9 を解くと x = ?", "choices": ["3", "4", "5", "6"], "answer": 2},
    ],
}

QUIZ_SIZE = 10  # 出題数

def _get_user_or_test():
    user_id = session.get("user_id")
    if user_id:
        return User.get_by_id(user_id)
    # テスト表示用：id=1 を探す／作成
    user = User.get_or_none(User.id == 1)
    if not user:
        user = User.create(name="テストユーザー")
    return user

@class1_bp.route("/class1")
def class1():
    user = _get_user_or_test()
    return render_template("class1.html", user=user)

@class1_bp.route("/class1/level<int:level>")
def class1_start(level):
    """クイズ開始：問題をランダム抽出してセッションに保存し、最初の問題へリダイレクト"""
    user = _get_user_or_test()
    if level not in QUESTIONS:
        return redirect(url_for("class1.class1"))

    pool = QUESTIONS[level][:]
    if len(pool) < QUIZ_SIZE:
        # 問題数が足りない場合は全問使用して重複を許す（通常は十分な問題を準備してください）
        selected = random.choices(pool, k=QUIZ_SIZE)
    else:
        selected = random.sample(pool, k=QUIZ_SIZE)

    # セッションに保存（JSON化可能な構造）
    session[f"class1_{level}_questions"] = selected
    session[f"class1_{level}_answers"] = []  # ユーザーの解答（選択肢インデックス）
    return redirect(url_for("class1.question", level=level, idx=0))

@class1_bp.route("/class1/level<int:level>/q/<int:idx>", methods=["GET", "POST"])
def question(level, idx):
    user = _get_user_or_test()
    questions = session.get(f"class1_{level}_questions")
    if not questions:
        # クイズ未初期化ならスタートページへ
        return redirect(url_for("class1.class1"))

    answers = session.get(f"class1_{level}_answers", [])

    # POST: 今の問いの回答を保存して次へ
    if request.method == "POST":
        choice = request.form.get("choice")
        try:
            choice_idx = int(choice)
        except (TypeError, ValueError):
            choice_idx = None
        # 回答を保存（欠答は None として保持）
        answers.append(choice_idx)
        session[f"class1_{level}_answers"] = answers

        # 次の問題または結果表示へ
        next_idx = idx + 1
        if next_idx >= len(questions):
            return redirect(url_for("class1.result", level=level))
        return redirect(url_for("class1.question", level=level, idx=next_idx))

    # GET: 指定 idx を表示
    if idx < 0 or idx >= len(questions):
        return redirect(url_for("class1.class1"))

    q = questions[idx]
    total = len(questions)
    progress = idx + 1
    # パーセンテージをサーバー側で計算してテンプレートに渡す（テンプレート内での式を避けるため）
    progress_percent = int((progress * 100) // total)
    return render_template("class1_level.html", user=user, level=level, q=q, idx=idx, total=total, progress=progress, progress_percent=progress_percent)

@class1_bp.route("/class1/level<int:level>/result")
def result(level):
    user = _get_user_or_test()
    questions = session.get(f"class1_{level}_questions", [])
    answers = session.get(f"class1_{level}_answers", [])

    correct = 0
    for qi, q in enumerate(questions):
        correct_answer = q.get("answer")
        user_choice = None
        if qi < len(answers):
            user_choice = answers[qi]
        if user_choice is not None and user_choice == correct_answer:
            correct += 1

    score = correct * 10  # 1問10点
    passed = score >= 80  # 合格ライン（80点以上）
    # 合格時のチケット付与（例）
    ticket_award = 0
    if passed:
        ticket_award = {1: 1, 2: 2, 3: 3}.get(level, 1)
        user.ticket += ticket_award
        user.save()

    # 結果表示のため、現在の質問と回答をテンプレートに渡す（表示後にセッションをクリア）
    q_copy = list(questions)
    a_copy = list(answers)

    # 結果表示後はセッションのクイズデータを削除
    session.pop(f"class1_{level}_questions", None)
    session.pop(f"class1_{level}_answers", None)

    return render_template("class1_result.html", user=user, level=level, score=score, correct=correct, total=len(questions), passed=passed, ticket_award=ticket_award, questions=q_copy, answers=a_copy)
# ...existing code...