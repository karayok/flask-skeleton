from typing import Dict

from flask_sqlalchemy_session import current_session

from myapp.database import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def get_users(id: int = None, name: str = None) -> [Dict]:
        query = current_session.query(User)
        query = query.filter_by(id=id) if id else query
        query = query.filter_by(name=name) if name else query
        users = query.all()
        return list(map(lambda user: {
            'id': user.id,
            'name': user.name,
        }, users)) if users else []


class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    score = db.Column(db.Integer)

    def __init__(self, user_id, score):
        self.user_id = user_id
        self.score = score

    def __repr__(self):
        return '<Score %r>' % self.score

    @staticmethod
    def create_score(user_id: int, score: int) -> int:
        score = Score(user_id, score)
        current_session.add(score)
        return score.id
