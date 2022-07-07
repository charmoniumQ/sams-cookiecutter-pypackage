import asyncio
from pathlib import Path
import os
import itertools
import shutil
from subprocess import run

from cookiecutter.main import cookiecutter
import toml
import pytest

@pytest.mark.parametrize("pypi_package,use_poetry", itertools.product(
    [True, False],
    [True, False]
))
def test_cookiecutter(pypi_package, use_poetry):
    dest = Path("build")
    repo_name = "my-test"
    version = "1.2.3"
    use_poetry = True

    if dest.exists():
        shutil.rmtree(dest)

    cookiecutter(
        template=str(Path()),
        output_dir=str(dest),
        no_input=True,
        overwrite_if_exists=True,
        extra_context={
            "repo_name": repo_name,
            "package_name": "my_test",
            "description": "Test package",
            "author_name": "A Author",
            "author_email": "person@exmaple.com",
            "license": "BSD-3-Clause",
            "__year": "2022",
            "repo_user": "me",
            "repo_url": "https://example.com",
            "version": version,
            "use_poetry": "yes" if use_poetry else "no",
            "pypi_package": "yes" if pypi_package else "no",
            "keywords": "cool awesome",
            "trove_license": "License :: OSI Approved :: BSD License,License :: OSI Approved :: MIT License",
            "trove_intended_audience": "Intended Audience :: Developers,Intended Audience :: Education",
            "trove_topics": "Topic :: Software Development :: Libraries :: Python Modules,Topic :: Software Development :: Libraries",
            "trove_classifiers": "",
            "nix_dependencies": "pkgs.hello pkgs.fortune",
        },
    )

    repo = dest / repo_name
    pyproject = toml.loads((repo / "pyproject.toml").read_text())
    env = {
        **{
            key: val
            for key, val in os.environ.items()
            if key not in {"VIRTUAL_ENV", "PYTHONNOUSERSITE", "PATH", "PLAT"}
        },
        "PATH": ":".join(
            path
            for path in os.environ["PATH"].split(":")
            if os.environ["VIRTUAL_ENV"] not in path
        )
    }
    if use_poetry:
        run(["git", "init"], check=True, cwd=repo, env=env)
        run(["git", "branch", "main"], check=True, cwd=repo, env=env)
        run(["git", "add", "-A"], check=True, cwd=repo, env=env)
        run(["git", "commit", "-m", "initial commit"], check=True, cwd=repo, env=env)
        nix_command = ["nix", "develop", "--command"]
        run([*nix_command, "hello"], check=True, cwd=repo, env=env)
        run([*nix_command, "fortune"], check=True, cwd=repo, env=env, capture_output=True)
        venv_path = run([*nix_command, "poetry", "env", "info", "--path"], check=True, cwd=repo, env=env, capture_output=True).stdout.strip()
        python_exe = run([*nix_command, "which", "python"], check=True, cwd=repo, env=env, capture_output=True).stdout.strip()
        assert venv_path + b"/bin/python" == python_exe, (venv_path + b"/bin/python", python_exe)
        run(["git", "add", "poetry.lock", "flake.lock"], check=True, cwd=repo, env=env)
        run(["git", "commit", "-m", "Add lockfiles"], check=True, cwd=repo, env=env)
        # I expect only these new files.
        # I will commit them so that I can test if I am creating any _other_ new files.
        run([*nix_command, "./script.py", "fmt"], check=True, cwd=repo, env=env)
        run([*nix_command, "./script.py", "test"], check=True, cwd=repo, env=env)
        run([*nix_command, "./script.py", "all-tests"], check=True, cwd=repo, env=env)
        proc = run(["git", "--no-pager", "diff"], check=True, cwd=repo, env=env, capture_output=True)
        assert not proc.stdout, "Running scripts should create no diff."
        assert any("License ::" in classifier for classifier in pyproject["tool"]["poetry"]["classifiers"])
    else:
        assert "poetry" not in pyproject["tool"]
    assert ("keywords" in pyproject["tool"]["poetry"]) == pypi_package
    assert ("classifiers" in pyproject["tool"]["poetry"]) == pypi_package


if __name__ == "__main__":
    test_cookiecutter(True, True)
