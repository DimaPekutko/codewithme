import sqlalchemy as sa

from .problem import Problem
from .problem_category import ProblemCategory

from db import Base
from db.models import *


class ProblemCatM2M(Base):
    __tablename__ = 'problems_categories'

    id = sa.Column(sa.Integer, primary_key=True)

    problem_id = sa.Column(sa.Integer, sa.ForeignKey(Problem.id, ondelete='CASCADE'))
    category_id = sa.Column(sa.Integer, sa.ForeignKey(ProblemCategory.id, ondelete='CASCADE'))
