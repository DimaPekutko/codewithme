import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .. import types

from db import TableWithDate
from db.models import *


class Problem(TableWithDate):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)

    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    complexity_level = Column(Integer, nullable=False)

    categories = relationship('ProblemCategory', secondary='problems_categories', lazy='joined')
    status = sa.Column(sa.Enum(types.ProblemStatus), nullable=False, default=types.ProblemStatus.disabled)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User')

    lang_problems = relationship('LangProblem', back_populates='problem')
