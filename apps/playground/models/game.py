import sqlalchemy as sa
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from .. import types

from db import TableWithDate
from db.models import *


class Game(TableWithDate):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)

    user1_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    user1 = relationship("User", back_populates="games", primaryjoin="User.id==Game.user1_id")

    user2_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    user2 = relationship("User", back_populates="games", primaryjoin="User.id==Game.user2_id")

    winner_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"))
    winner = relationship("User", back_populates="winned_games", primaryjoin="User.id==Game.winner_id")

    lang_problem_id = sa.Column(sa.Integer, sa.ForeignKey("lang_problems.id", ondelete="CASCADE"), nullable=False)
    lang_problem = relationship("LangProblem", back_populates="games")

    status = sa.Column(sa.Enum(types.GameStatus), nullable=False, default=types.GameStatus.active)
    room_uid = sa.Column(sa.String, nullable=False)

    runtimes = relationship("Runtime", back_populates="game")
