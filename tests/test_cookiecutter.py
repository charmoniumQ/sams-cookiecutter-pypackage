import asyncio
from pathlib import Path
import os
import shutil
from subprocess import run

from cookiecutter.main import cookiecutter
import toml


def test_cookiecutter():
    dest = Path("build")
    repo_name = "my-test"
    version = "1.2.3"
    use_poetry = True
    pypi_package = True

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
        **os.environ,
        "PATH": ":".join([
            path
            for path in os.environ["PATH"].split(":")
            if path != os.environ["VIRTUAL_ENV"]
        ]),
        "VIRTUAL_ENV": "",
        "PIP_PYTHON_PATH": "",
        "PIPENV_ACTIVE": "",
        "PIP_DISABLE_PIP_VERSION_CHECK": "",
        "PYTHONNOUSERSITE": "",
    }
    run(["git", "init"], check=True, cwd=repo, env=env)
    run(["git", "add", "-A"], check=True, cwd=repo, env=env)
    run(["git", "commit", "-m", "test"], check=True, cwd=repo, env=env)
    nix_command = ["nix", "develop", "--command"]
    run([*nix_command, "hello"], check=True, cwd=repo, env=env)
    run([*nix_command, "fortune"], check=True, cwd=repo, env=env)
    # I expect only these new files.
    # I will commit them so that I can test if I am creating any _other_ new files.
    run(["git", "add", "poetry.lock", "flake.lock"], check=True, cwd=repo, env=env)
    run(["git", "commit", "-m", "test"], check=True, cwd=repo, env=env)
    if use_poetry:
        # We should have Python packages in here.
        run([*nix_command, "./script.py", "fmt"], check=True, cwd=repo, env=env)
        run([*nix_command, "./script.py", "test"], check=True, cwd=repo, env=env)
        run([*nix_command, "./script.py", "all-tests"], check=True, cwd=repo, env=env)
        proc = run(["git", "diff"], check=True, cwd=repo, env=env, capture_output=True)
        assert not proc.stdout, "Running scripts should create no diff."
        assert any("License ::" in classifier for classifier in pyproject["tool"]["poetry"]["classifiers"])
    else:
        assert "poetry" not in pyproject["tool"]
    assert ("keywords" in pyproject["tool"]["poetry"]) == pypi_package
    assert ("classifiers" in pyproject["tool"]["poetry"]) == pypi_package


if __name__ == "__main__":
    test_cookiecutter()
