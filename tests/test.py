import itertools
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List, Mapping, TypeVar, Union

from cookiecutter.main import cookiecutter

POD = Union[bool, int, float, str]
T = TypeVar("T")
V = TypeVar("V")
project_root = Path(__file__).parent.parent


def test_template() -> None:
    for context in expand(context_spec):
        with tempfile.TemporaryDirectory() as dirf_str:
            dirf = Path(dirf_str)
            cookiecutter(
                str(project_root),
                no_input=True,
                extra_context=context,
                output_dir=dirf,
            )
            verify(dirf, context)


context_spec: Mapping[str, List[POD]] = {
    "package_name": ["nameless"],
    "cli": [True, False],
}


def verify(dirf: Path, context: Mapping[str, POD]) -> None:
    if context["cli"]:
        subprocess.run(["poetry", "run", context["package_name"]], cwd=dirf)


def expand(spec: Mapping[T, Iterable[V]]) -> Iterable[Mapping[T, V]]:
    for values_choice in itertools.product(*spec.values()):
        yield dict(zip(spec.keys(), values_choice))
