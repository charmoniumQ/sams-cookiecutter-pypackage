#!/usr/bin/env sh

set -e -x

cd "$(dirname "${0}")/.."

poetry run sphinx-build -q -W -b html docs docs/_build
