from flask import Flask
from models import db, User
from routes import main_bp, class1_bp

def create_app():
    """Flaskアプリケーション作成"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    # データベーステーブル作成
    db.create_tables([User], safe=True)

    # Blueprint登録
    app.register_blueprint(main_bp)
    app.register_blueprint(class1_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
