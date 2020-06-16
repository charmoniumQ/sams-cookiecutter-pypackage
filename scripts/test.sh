#!/bin/bash

cd "$(dirname "${0}")/.."

#package=
src="./hooks ./scripts ./stubs"
check=$([ "${1}" = "check" ] && echo "true" || echo "")
verbose=${verbose:-}
skip_lint=${skip_lint:-}

function now() {
	python -c 'import datetime; print((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())'
}

function capture() {
	local log=$(mktemp)
	local command=("${@}")

	local command_start="$(now)"
	"${command[@]}" &> "${log}"
	local command_exit="${?}"
	local command_end="$(now)"
	local command_duration=$(python3 -c "print('{:.2f}'.format(${command_end} - ${command_start}))")

	if [ -s "${log}" -o "${command_exit}" -ne 0 -o -n "${verbose}" ]; then
		if [ "${command_exit}" -eq 0 ]; then
			echo -e "\033[32;1m\$ ${command[@]}\033[0m"
			cat "${log}"
			echo -e "\033[32;1mexitted ${command_exit} in ${command_duration}s\033[0m"
		else
			echo -e "\033[31;1m\$ ${command[@]}\033[0m"
			cat "${log}"
			echo -e "\033[31;1mexitted ${command_exit} in ${command_duration}s\033[0m"
			exit "${command_exit}"
		fi
	fi
}

[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			autoflake --recursive $([ -n "${check}" ] && echo "--check" || echo "--in-place") ${src} tests

[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			isort --recursive $([ -n "${check}" ] && echo "--check-only") ${src} tests

[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			black --quiet --target-version py38 $([ -n "${check}" ] && echo "--check") ${src} tests

[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			sh -c "pylint ${src} tests || poetry run pylint-exit -efail \${?} > /dev/null"

capture \
	poetry run \
		env PYTHONPATH=".:${PYTHONPATH}" MYPYPATH="./stubs:${MYPYPATH}" \
			dmypy run -- ${src} tests

capture \
	poetry run \
		pytest -vvv --quiet --exitfirst tests
