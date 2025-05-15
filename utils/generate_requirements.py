import os
import tomllib

pyproject_path = os.path.join(os.getcwd(), "pyproject.toml")

with open(pyproject_path, "rb") as f:
    data = tomllib.load(f)

deps = data["project"]["dependencies"]

with open("requirements.txt", "w") as out:
    for dep in deps:
        out.write(dep + "\n")
