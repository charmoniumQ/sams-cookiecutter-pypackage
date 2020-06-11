#!/usr/bin/env sh

cd "$(dirname "${0}")/.."

output_dir=build
rm -rf "${output_dir}"
cookiecutter . --no-input --output-dir "${output_dir}"
echo "${output_dir}/nameless/"
