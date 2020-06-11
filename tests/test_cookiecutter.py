import itertools
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List, Mapping, TypeVar

import pytest
from cookiecutter.exceptions import CookiecutterException
from cookiecutter.main import cookiecutter
from tqdm import tqdm

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
    "coverage",
    "codecov",
]


context_spec: Mapping[str, List[str]] = {
    "package_name": ["nameless"],
    "repository_name": ["nameless"],
    "enable_cli": ["y", "n"],
    "enable_resource_directory": ["y", "n"],
    "license_name": ["NCSA"],
    **{f"enable_{option}": ["y", "n"] for option in tools},
}


def verify(out_dir: Path, context: Mapping[str, str]) -> None:
    proj_root = out_dir / context["repository_name"]

    subprocess.run(
        ["poetry", "check"], cwd=proj_root, check=True,
    )

    subprocess.run(
        ["poetry", "install"], cwd=proj_root, check=True, capture_output=True,
    )

    if context["enable_cli"] == "y":
        subprocess.run(
            ["poetry", "run", context["package_name"]], cwd=proj_root, check=True,
        )
    else:
        assert not (proj_root / context["package_name"] / "cli.py").exists()

    if context["enable_resource_directory"] == "y":
        # TODO: assert resource dir exists in install
        pass
    else:
        assert not (proj_root / "res").exists()

    try:
        script_test = subprocess.run(
            ["./scripts/test.sh"],
            cwd=proj_root,
            env=dict(**os.environ, verbose="true"),
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as err:
        print(err.stdout)
        print(err.stderr)
        raise err

    for tool in tools:
        tool_enabled = context[f"enable_{tool}"] == "y"
        if tool == "mypy":
            tool = "dmypy"
        tool_present = f" {tool} ".encode() in script_test.stdout

        # when assertion fails, give ma chance to see stdout
        if tool_present != tool_enabled:
            print(script_test.stdout.decode())
        assert tool_present == tool_enabled, (tool, tool_present, tool_enabled)

    if context["enable_pylint"] == "n":
        assert not (proj_root / ".pylintrc").exists()

    if context["enable_mypy"] == "n":
        assert not (proj_root / "mypy.ini").exists()

    if context["enable_codecov"] == "y":
        assert "codecov" in read_file(proj_root / "TODO.md")

    if context["license_name"].lower() == "ncsa":
        assert "NCSA" in read_file(proj_root / "LICENSE.txt")

    script_test = subprocess.run(
        ["./scripts/docs.sh"],
        cwd=proj_root,
        env=dict(**os.environ, verbose="true"),
        capture_output=True,
        check=True,
    )

    assert (proj_root / "docs" / "_build" / "index.html").exists()


def expand(spec: Mapping[T, Iterable[V]]) -> Iterable[Mapping[T, V]]:
    options = list(itertools.product(*spec.values()))
    # test first, last, and some in between
    # Usually, these options to not "interfere" with each other
    # So no need to test each possible configuration (exponential)
    some_options = [options[0], options[-1], *options[1:-1:257]]
    for values_choice in tqdm(some_options):
        yield dict(zip(spec.keys(), values_choice))


def read_file(file_name: Path) -> str:
    with open(file_name) as file_obj:
        return file_obj.read()


if __name__ == "__main__":
    test_cookiecutter()
