from enum import Enum


class Language(Enum):
    python = 'python'
    js = 'js'
    cpp = 'cpp'


class ProblemStatus(Enum):
    active = 'active'
    disabled = 'disabled'


class ProblemLangStatus(Enum):
    active = 'active'
    disabled = 'disabled'
