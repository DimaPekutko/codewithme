import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import TableWithDate
from db.models import *
from .. import types


class LangProblem(TableWithDate):
    __tablename__ = 'lang_problems'

    id = sa.Column(sa.Integer, primary_key=True)

    language = sa.Column(sa.Enum(types.Language), nullable=False)

    code_context = sa.Column(sa.String, nullable=False)
    initial_code = sa.Column(sa.String, nullable=False)

    status = sa.Column(sa.Enum(types.ProblemLangStatus),
                       nullable=False,
                       server_default=types.ProblemLangStatus.disabled.value)

    problem_id = sa.Column(sa.Integer, sa.ForeignKey('problems.id', ondelete='CASCADE'))
    problem = relationship('Problem', back_populates='lang_problems')

    assertions = relationship('CodeAssertion', back_populates='lang_problem')

    runtimes = relationship('Runtime', back_populates='lang_problem')
    games = relationship('Game',
                         back_populates='lang_problem',
                         primaryjoin="LangProblem.id==Game.lang_problem_id")
