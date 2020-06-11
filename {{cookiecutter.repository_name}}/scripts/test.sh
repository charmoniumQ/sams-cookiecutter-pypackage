#!/bin/bash

cd "$(dirname "${0}")/.."

check=${check:-}
verbose=${verbose:-}
skip_lint=${skip_lint:-}
htmlcov=${htmlcov:-}
codecov=${codecov:-}

package={{cookiecutter.package_name}}
src="./${package}"

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
			echo -e "\033[32;1m\$ ${command[@]} \033[0m"
			cat "${log}"
			echo -e "\033[32;1mexitted ${command_exit} in ${command_duration}s\033[0m"
		else
			echo -e "\033[31;1m\$ ${command[@]} \033[0m"
			cat "${log}"
			echo -e "\033[31;1mexitted ${command_exit} in ${command_duration}s\033[0m"
			exit "${command_exit}"
		fi
	fi
}

{%- if cookiecutter.enable_autoflake == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			autoflake --recursive $([ -n "${check}" ] && echo "--check" || echo "--in-place") "${src}" tests
{%- endif %}

{%- if cookiecutter.enable_isort == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			isort --recursive $([ -n "${check}" ] && echo "--check-only") "${src}" tests
{%- endif %}

{%- if cookiecutter.enable_black == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			black --quiet --target-version py38 $([ -n "${check}" ] && echo "--check") "${src}" tests
{%- endif %}

{%- if cookiecutter.enable_pylint == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			sh -c "pylint ${src} tests || poetry run pylint-exit -efail \${?} > /dev/null"
{%- endif %}

{%- if cookiecutter.enable_mypy == "y" %}
capture \
	poetry run \
		env PYTHONPATH="$(dirname "${src}"):${PYTHONPATH}" \
			dmypy run -- tests
{%- endif %}

{%- if cookiecutter.enable_pytest == "y" %}
capture \
	poetry run \
		pytest --quiet --cov="${src}" --cov=tests --cov-report=term-missing --exitfirst
{%- endif %}

{%- if cookiecutter.enable_bandit == "y" %}
capture \
	poetry run \
		env PYTHONPATH="$(dirname "${src}"):${PYTHONPATH}" \
			bandit --recursive "${src}"
{%- endif %}

{%- if cookiecutter.enable_coverage == "y" %}
capture \
	poetry run \
		coverage html -d htmlcov
if [[ -n "${htmlcov}" ]]; then
	xdg-open htmlcov/index.html
fi
{%- endif %}

{%- if cookiecutter.enable_codecov == "y" %}
capture \
	poetry run \
		codecov
{%- endif %}
