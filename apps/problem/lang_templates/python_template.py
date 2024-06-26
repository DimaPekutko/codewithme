DEFAULT_CONTEXT = """# define some context here (e.g. types for arguments)"""

DEFAULT_INIT = """# function should have name 'main'
def main(arg1: int, arg2: str, *args, **kwargs):
    pass
"""

DEFAULT_ASSERT = """assert True"""

RUNTIME_TEMPLATE = """
# PYTHON: autogenerated runtime code
import traceback
import json

# context
{code_context}
# initial code
{initial_code}

result = {{
    'errors': [],
    'passed': 0,
    'failed': 0
}}

# assertions
{asserts}

print(json.dumps(result))
"""

RUNTIME_ASSERT = """
try:
    {code}
except AssertionError:
    error = str(traceback.format_exc())

    result['failed'] += 1
    result['errors'].append(error)
else:
    result['passed'] += 1
"""
