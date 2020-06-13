#!/usr/bin/env sh

cd "$(dirname "${0}")/.."

output_dir=.
rm -rf "${output_dir}/nameless"
cookiecutter . --no-input --output-dir "${output_dir}"
# echo "${output_dir}/nameless/"
