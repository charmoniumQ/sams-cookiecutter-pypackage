from __future__ import annotations

import itertools
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, TypeVar, Union

import pytest
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter

T = TypeVar("T")
V = TypeVar("V")
project_root = Path(__file__).parent.parent


def test_cookiecutter() -> None:
    for context in expand(context_spec):
        with tempfile.TemporaryDirectory() as out_dir_str:
            out_dir = Path(out_dir_str)
            if (
                context["enable_codecov"] == "y" or context["enable_coverage"] == "y"
            ) and context["enable_pytest"] == "n":
                print("expect failure")
                with pytest.raises(CookiecutterException):
                    cookiecutter(
                        str(project_root),
                        no_input=True,
                        extra_context=context,
                        output_dir=str(out_dir),
                    )
            else:
                cookiecutter(
                    str(project_root),
                    no_input=True,
                    extra_context=context,
                    output_dir=str(out_dir),
                )
                verify(out_dir, context)


tools = [
    "autoflake",
    "isort",
    "black",
    "pylint",
    "bandit",
    "mypy",
    "pytest",
]


context_spec: Mapping[str, List[str]] = {
    "package_name": ["nameless"],
    "repository_name": ["nameless"],
    "enable_cli": ["y", "n"],
    "enable_resource_directory": ["y", "n"],
    "license_spdx": ["NCSA"],
    **{f"enable_{option}": ["y", "n"] for option in tools},
    "enable_sphinx": ["y", "n"],
    "enable_codecov": ["y", "n"],
    "enable_coverage": ["y", "n"],
    "initial_commit": ["y"],
    "code_of_conduct": ["none", "contributor-covenant"],
    "enable_bump2version": ["y", "n"],
    "pypi_package": ["y", "n"],
}


def verify(out_dir: Path, context: Mapping[str, str]) -> None:
    test_proj = out_dir / context["repository_name"]

    def subprocess_run(
        cmd: List[str], env: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> subprocess.CompletedProcess[bytes]:
        if not env:
            env = {}
        try:
            return subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                cwd=test_proj,
                env={**os.environ, **env},
                **kwargs,
            )
        except subprocess.CalledProcessError as err:
            hbar = "-" * 40
            print(f"{hbar} stdout {hbar}")
            sys.stdout.buffer.write(err.stdout)
            print(f"{hbar}--------{hbar}")
            print(f"{hbar} stderr {hbar}")
            sys.stdout.buffer.write(err.stderr)
            print(f"{hbar}--------{hbar}")
            raise err

    subprocess_run(["poetry", "check"])

    subprocess_run(["poetry", "install"])

    if context["enable_cli"] == "y":
        subprocess_run(["poetry", "run", context["package_name"]])
    else:
        assert not (test_proj / context["package_name"] / "cli.py").exists()

    if context["enable_resource_directory"] == "y":
        # TODO: assert resource dir exists in install
        pass
    else:
        assert not (test_proj / "res").exists()

    script_test = subprocess_run(
        ["./scripts/test.sh"], env=dict(**os.environ, verbose="true"),
    )

    for tool in tools:
        tool_enabled = context[f"enable_{tool}"] == "y"
        if tool == "mypy":
            tool = "dmypy"
        tool_present = f" {tool} ".encode() in script_test.stdout

        # when assertion fails, give ma chance to see stdout
        if tool_present != tool_enabled:
            print(script_test.stdout.decode())
        assert tool_present == tool_enabled, (tool, tool_present, tool_enabled)

    if context["enable_mypy"] == "y":
        assert (test_proj / "stubs").exists()

    assert (context["enable_codecov"] == "y") == (
        "codecov" in read_file(test_proj / "scripts/test.sh")
    )
    assert (context["enable_coverage"] == "y") == (
        "coverage" in read_file(test_proj / "scripts/test.sh")
    )

    if (
        context["enable_codecov"] == "y" or context["enable_coverage"] == "y"
    ) and context["enable_pytest"] == "y":
        assert "--cov" in script_test.stdout.decode()

    if context["enable_pylint"] == "n":
        assert not (test_proj / ".pylintrc").exists()

    if context["enable_mypy"] == "n":
        assert not (test_proj / "mypy.ini").exists()

    if context["enable_codecov"] == "y":
        assert "codecov" in read_file(test_proj / "TODO.md")

    if context["license_spdx"].lower() == "ncsa":
        assert "NCSA" in read_file(test_proj / "LICENSE.txt")

    if context["enable_sphinx"] == "y":
        script_test = subprocess_run(["./scripts/docs.sh"], env=dict(verbose="true"),)
        assert (test_proj / "docs/_build/index.html").exists()
        assert "autoapi/nameless/_lib/index" in read_file(
            test_proj / "docs/_doctest/output.txt"
        )
    else:
        assert not (test_proj / "docs").exists()
        assert not (test_proj / "scripts/docs.sh").exists()

    if context["initial_commit"] == "y":
        assert subprocess_run(["git", "status", "porcelain"])

    if context["code_of_conduct"] == "contributor-covenant":
        assert "Contributor Covenant Code of Conduct" in read_file(
            test_proj / "CODE_OF_CONDUCT"
        )
    else:
        assert not (test_proj / "CODE_OF_CONDUCT").exists()

    script_test = subprocess_run(
        ["./scripts/publish.sh", "patch"],
        env=dict(skip_test="true", skip_docs="true", dry_run="true"),
    )

    assert (context["pypi_package"] == "y") == (
        "poetry publish" in read_file(test_proj / "scripts/publish.sh")
    )
    assert "./scripts/test.sh" in read_file(test_proj / "scripts/publish.sh")
    assert (context["enable_sphinx"] == "y") == (
        "./scripts/docs.sh" in read_file(test_proj / "scripts/publish.sh")
    )
    assert (context["enable_bump2version"] == "y") == (
        "bump2version" in read_file(test_proj / "scripts/publish.sh")
    )

    assert (context["enable_bump2version"] == "y") == (
        test_proj / ".bumpversion.cfg"
    ).exists()


def expand(spec: Mapping[T, Iterable[V]]) -> Iterable[Mapping[T, V]]:
    options = list(itertools.product(*spec.values()))
    # test first, last, and some in between
    # Usually, these options to not "interfere" with each other
    # So no need to test each possible configuration (exponential)
    some_options = [options[0], options[-1], *random.sample(options, 2)]
    for values_choice in some_options:
        yield dict(zip(spec.keys(), values_choice))


def read_file(file_name: Union[bytes, str, Path]) -> str:
    with open(file_name) as file_obj:
        return file_obj.read()


if __name__ == "__main__":
    test_cookiecutter()
