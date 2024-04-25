import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import Base
from db.models import *


class CodeAssertion(Base):
    __tablename__ = 'code_assertions'

    id = sa.Column(sa.Integer, primary_key=True)
    code = sa.Column(sa.String, nullable=False)

    lang_problem_id = sa.Column(sa.Integer, sa.ForeignKey('lang_problems.id', ondelete='CASCADE'))
    lang_problem = relationship('LangProblem', back_populates='assertions')
