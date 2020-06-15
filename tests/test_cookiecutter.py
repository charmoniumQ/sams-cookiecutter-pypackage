from __future__ import annotations

import itertools
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, List, Mapping, TypeVar

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
}


def verify(out_dir: Path, context: Mapping[str, str]) -> None:
    proj_root = out_dir / context["repository_name"]

    subprocess_run(
        ["poetry", "check"], cwd=proj_root,
    )

    subprocess_run(
        ["poetry", "install"], cwd=proj_root,
    )

    if context["enable_cli"] == "y":
        subprocess_run(
            ["poetry", "run", context["package_name"]], cwd=proj_root,
        )
    else:
        assert not (proj_root / context["package_name"] / "cli.py").exists()

    if context["enable_resource_directory"] == "y":
        # TODO: assert resource dir exists in install
        pass
    else:
        assert not (proj_root / "res").exists()

    script_test = subprocess_run(
        ["./scripts/test.sh"], cwd=proj_root, env=dict(**os.environ, verbose="true"),
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

    assert (context["enable_codecov"] == "y") == (
        "codecov" in read_file(proj_root / "scripts" / "test.sh")
    )
    assert (context["enable_coverage"] == "y") == (
        "coverage" in read_file(proj_root / "scripts" / "test.sh")
    )

    if (
        context["enable_codecov"] == "y" or context["enable_coverage"] == "y"
    ) and context["enable_pytest"] == "y":
        assert "--cov" in script_test.stdout.decode()

    if context["enable_pylint"] == "n":
        assert not (proj_root / ".pylintrc").exists()

    if context["enable_mypy"] == "n":
        assert not (proj_root / "mypy.ini").exists()

    if context["enable_codecov"] == "y":
        assert "codecov" in read_file(proj_root / "TODO.md")

    if context["license_spdx"].lower() == "ncsa":
        assert "NCSA" in read_file(proj_root / "LICENSE.txt")

    if context["enable_sphinx"] == "y":
        script_test = subprocess_run(
            ["./scripts/docs.sh"],
            cwd=proj_root,
            env=dict(**os.environ, verbose="true"),
        )
        assert (proj_root / "docs" / "_build" / "index.html").exists()
    else:
        assert not (proj_root / "docs").exists()
        assert not (proj_root / "scripts" / "docs.sh").exists()

    if context["initial_commit"] == "y":
        assert subprocess_run(["git", "status", "porcelain"])

    if context["code_of_conduct"] == "contributor-covenant":
        assert "Contributor Covenant Code of Conduct" in read_file(
            proj_root / "CODE_OF_CONDUCT"
        )
    else:
        assert not (proj_root / "CODE_OF_CONDUCT").exists()


def expand(spec: Mapping[T, Iterable[V]]) -> Iterable[Mapping[T, V]]:
    options = list(itertools.product(*spec.values()))
    # test first, last, and some in between
    # Usually, these options to not "interfere" with each other
    # So no need to test each possible configuration (exponential)
    some_options = [options[0], options[-1], *random.sample(options, 2)]
    for values_choice in some_options:
        yield dict(zip(spec.keys(), values_choice))


def subprocess_run(cmd: List[str], **kwargs: Any) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(cmd, check=True, capture_output=True, **kwargs)
    except subprocess.CalledProcessError as err:
        hbar = "-" * 40
        print(f"{hbar} stdout {hbar}")
        sys.stdout.buffer.write(err.stdout)
        print(f"{hbar}--------{hbar}")
        print(f"{hbar} stderr {hbar}")
        sys.stdout.buffer.write(err.stderr)
        print(f"{hbar}--------{hbar}")
        raise err


def read_file(file_name: Path) -> str:
    with open(file_name) as file_obj:
        return file_obj.read()


if __name__ == "__main__":
    test_cookiecutter()
