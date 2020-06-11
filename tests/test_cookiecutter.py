import itertools
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List, Mapping, TypeVar

from cookiecutter.main import cookiecutter
from tqdm import tqdm

T = TypeVar("T")
V = TypeVar("V")
project_root = Path(__file__).parent.parent


def test_cookiecutter() -> None:
    for context in expand(context_spec):
        with tempfile.TemporaryDirectory() as out_dir_str:
            out_dir = Path(out_dir_str)
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
    **{
        f"enable_{option}": ["y"]
        # f"enable_{option}": ["y", "n"]
        for option in tools
    },
}


def verify(out_dir: Path, context: Mapping[str, str]) -> None:
    proj_root = out_dir / context["repository_name"]

    subprocess.run(
        ["poetry", "check"], cwd=proj_root, check=True, capture_output=True,
    )

    subprocess.run(
        ["poetry", "install"], cwd=proj_root, check=True, capture_output=True,
    )

    if context["enable_cli"] == "y":
        subprocess.run(
            ["poetry", "run", context["package_name"]], cwd=proj_root, check=True,
        )
        # TODO: assert package_name on the path in install
    else:
        assert not (proj_root / context["package_name"] / "cli.py").exists()

    if context["enable_resource_directory"] == "y":
        # TODO: assert resource dir exists in install
        pass
    else:
        assert not (proj_root / "res").exists()

    # pylint: disable=subprocess-run-check
    script_test = subprocess.run(
        ["./scripts/test.sh"],
        cwd=proj_root,
        env=dict(**os.environ, verbose="true"),
        capture_output=True,
    )

    if script_test.returncode != 0:
        # when check fails, give me a chance to see stdout
        print(script_test.stdout.decode())
        assert script_test.returncode == 0

    for tool in tools:
        assert (context[f"enable_{tool}"] == "y") == (
            tool.encode() in script_test.stdout
        )

    if context["enable_codecov"] == "y":
        with (proj_root / "TODO.md").open("r") as todos:
            assert "codecov" in todos.read()


def expand(spec: Mapping[T, Iterable[V]]) -> Iterable[Mapping[T, V]]:
    for values_choice in tqdm(list(itertools.product(*spec.values()))):
        yield dict(zip(spec.keys(), values_choice))


if __name__ == "__main__":
    test_cookiecutter()
