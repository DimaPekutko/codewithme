from tempfile import NamedTemporaryFile
import os
import sys

code = sys.stdin.read()

scriptFile = NamedTemporaryFile(delete=True, suffix=".py")
with open(scriptFile.name, "w") as f:
    f.write(code)
    os.chmod(scriptFile.name, 777)

os.system(f"python {scriptFile.name}")
