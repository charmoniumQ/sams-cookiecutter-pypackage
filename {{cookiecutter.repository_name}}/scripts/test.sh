#!/bin/bash

cd "$(dirname "${0}")/.."

check=${check:-}
verbose=${verbose:-}
skip_lint=${skip_lint:-}
htmlcov=${htmlcov:-}
{%- if cookiecutter.enable_codecov == "y" %}
codecov=${codecov:-}
{%- endif %}

package={{cookiecutter.package_name}}
package_loc=$(dirname "${PWD}/${package}")
other_srcs="tests/ $(find scripts/ -name '*.py' -printf '%p ')"
{%- if cookiecutter.enable_sphinx == "y" %}
other_srcs="${other_srcs} docs/conf.py"
{%- endif %}

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

flag_verbose_or_quiet=$([ -n "${verbose}" ] && echo "--verbose" || echo "--quiet")
flag_verbose=$([ -n "${verbose}" ] && echo "--verbose")
flag_check_or_in_place=$([ -n "${check}" ] && echo "--check" || echo "--in-place")
flag_check_only=$([ -n "${check}" ] && echo "--check-only")
flag_check=$([ -n "${check}" ] && echo "--check")

{% if cookiecutter.enable_autoflake == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			autoflake --recursive ${flag_check_or_in_place} "${package}" ${other_srcs}
{% endif %}

{%- if cookiecutter.enable_isort == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			isort --recursive ${flag_check_only} "${package}"
# I can't enable isort in tests because mocking requires a specific import-order
{% endif %}

{%- if cookiecutter.enable_black == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			black --quiet --target-version py38 ${flag_check} ${flag_verbose_or_quiet} "${package}" ${other_srcs}
{% endif %}

{%- if cookiecutter.enable_pylint == "y" %}
[[ -n "${skip_lint}" ]] || \
	capture \
		poetry run \
			sh -c "pylint ${flag_verbose} ${package} ${other_srcs} || poetry run pylint-exit -efail \${?} > /dev/null"
{% endif %}

{%- if cookiecutter.enable_mypy == "y" %}
capture \
	poetry run \
		env PYTHONPATH="${package_loc}:${PYTHONPATH}" \
			dmypy run -- ${flag_verbose} ${other_srcs} $(find "${package}" -name '*.py')
{% endif %}

{%- if cookiecutter.enable_pytest == "y" %}
capture \
	poetry run \
		pytest --quiet --exitfirst {% if cookiecutter.enable_coverage == "y" or cookiecutter.enable_codecov %} --cov="${package}" --cov-report=term-missing {% endif %} tests
# I only care about --cov= in the exported package
{% endif %}

{%- if cookiecutter.enable_bandit == "y" %}
capture \
	poetry run \
		env PYTHONPATH="${package_loc}:${PYTHONPATH}" \
			bandit --recursive ${flag_verbose_or_quiet} "${package}"
# I only care about vulns in the exported package
{% endif %}

{%- if cookiecutter.enable_coverage %}
[[ -z "${htmlcov}" ]] || \
	xdg-open htmlcov/index.html
{% endif %}

{%- if cookiecutter.enable_coverage == "y" %}
poetry run \
	coverage html -d htmlcov
{% endif %}

{%- if cookiecutter.enable_codecov == "y" %}
[[ -z "${CODECOV_TOKEN}" ]] || \
	capture \
		poetry run \
			codecov
{% endif %}
