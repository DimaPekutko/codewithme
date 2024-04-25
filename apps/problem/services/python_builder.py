import ast

from .problem_lang_builder import ProblemLangBuilder
from .. import schemas
from .. import lang_templates


class PythonBuilder(ProblemLangBuilder):
    @staticmethod
    async def build_code(lpropblem: schemas.LangProblem) -> str:
        asserts = "\n".join(
            [
                lang_templates.python.RUNTIME_ASSERT.format(code="\n    ".join(_assert.code.split("\n")))
                for _assert in lpropblem.assertions
            ]
        )

        code = lang_templates.python.RUNTIME_TEMPLATE.format(asserts=asserts, **lpropblem.model_dump())

        try:
            ast.parse(code)
        except SyntaxError as err:
            raise ValueError(str(err.args))

        return code
