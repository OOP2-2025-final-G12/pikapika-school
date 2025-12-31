from models.db import db
from models.user import User
from routes.game import game_bp
blueprints = [
    game_bp
]

__all__ = ["db", "User", "blueprints"]
