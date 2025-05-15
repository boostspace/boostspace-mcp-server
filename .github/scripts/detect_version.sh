#!/usr/bin/env bash
# ---------------------------------------------
# Detect whether the version in pyproject.toml
# is newer than the latest v* git tag.
# Exposes outputs for GitHub Actions.
# ---------------------------------------------

set -euo pipefail

curr_version=$(
  python - <<'PY'
import tomllib, pathlib, sys
print(
    tomllib.loads(
        pathlib.Path("pyproject.toml").read_text(encoding="utf-8")
    )["project"]["version"]
)
PY
)
echo "current=${curr_version}" >> "${GITHUB_OUTPUT}"

git fetch --tags --quiet
last_tag=$(git tag --list 'v*' --sort=-v:refname | head -n1 | sed 's/^v//')
echo "previous=${last_tag}" >> "${GITHUB_OUTPUT}"

if [[ "$curr_version" != "$last_tag" ]]; then
  echo "publish=true" >> "${GITHUB_OUTPUT}"
fi
