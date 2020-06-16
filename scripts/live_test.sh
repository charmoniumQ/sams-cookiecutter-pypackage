#!/usr/bin/env sh

cd "$(dirname "${0}")/.."

output_dir=.
rm -rf "${output_dir}/ch-nameless"
cookiecutter . --no-input --output-dir "${output_dir}"
cd "${output_dir}/ch-nameless/"
