import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import TableWithDate
from db.models import *


class ProblemCategory(TableWithDate):
    __tablename__ = 'pcategories'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=True)

    problems = relationship('Problem', secondary='problems_categories')
