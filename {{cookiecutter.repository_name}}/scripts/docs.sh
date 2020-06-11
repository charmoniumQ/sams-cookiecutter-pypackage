#!/usr/bin/env sh

cd "$(dirname "${0}")/.."

sphinx-build -b html docs docs/_build
