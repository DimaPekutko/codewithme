import sqlalchemy as sa
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime
from .. import types

from db import TableWithDate
from db.models import *


class Runtime(TableWithDate):
    __tablename__ = 'runtimes'

    id = Column(Integer, primary_key=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='runtimes')

    lang_problem_id = sa.Column(sa.Integer, sa.ForeignKey('lang_problems.id', ondelete='CASCADE'), nullable=False)
    lang_problem = relationship('LangProblem',
                                back_populates='runtimes',
                                primaryjoin="LangProblem.id==Runtime.lang_problem_id")

    game_id = sa.Column(sa.Integer, sa.ForeignKey('games.id', ondelete='SET NULL'))
    game = relationship('Game',
                        back_populates='runtimes',
                        primaryjoin="Game.id==Runtime.game_id")

    status = sa.Column(sa.Enum(types.RuntimeStatus), nullable=False, default=types.RuntimeStatus.processing)

    code = sa.Column(String, nullable=False)
    tests_passed = Column(Integer)
    tests_failed = Column(Integer)
    output = sa.Column(String)

    finish_date = Column(DateTime(timezone=True))
