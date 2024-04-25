from scripts.db_session import db_session
from apps.problem.models import ProblemCategory


def perform(*args, **kwargs):
    categories = [
        ProblemCategory(name='Math'),
        ProblemCategory(name='Trees'),
        ProblemCategory(name='Arrays'),
        ProblemCategory(name='Graphs'),
        ProblemCategory(name='Backtracking'),
        ProblemCategory(name='DP1'),
        ProblemCategory(name='DP2'),
    ]
    db_session.add_all(categories)
    db_session.commit()
