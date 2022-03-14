import asyncio
from pathlib import Path
import os
import shutil
from subprocess import run

#from charmonium.async_subprocess import run as async_run
from cookiecutter.main import cookiecutter

dest = Path("build")
repo_name = "my-test"

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
        "repo_user": "me",
        # "repo_url": "me",
        "keywords": "cool awesome",
        "trove_classifiers": "",
        "version": "0.1.0",
	"trove_classifiers": "",
        "nix_dependencies": "",
    },
)

repo = dest / repo_name
virtual_env = os.environ["VIRTUAL_ENV"]
path_var = ":".join([
    path
    for path in os.environ["PATH"].split(":")
    if path != virtual_env
])
print("nix developing...")
run(
    ["nix", "develop", "--command", "true"],
    check=True,
    cwd=repo,
    env={
        **os.environ,
        "VIRTUAL_ENV": "",
        "PATH": path_var,
    },
)
print("done")
run(
    ["nix", "develop", "--command", "./script.py", "fmt"],
    check=True,
    cwd=repo,
    env={
        **os.environ,
        "VIRTUAL_ENV": "",
        "PATH": path_var,
    },
)
run(
    ["nix", "develop", "--command", "./script.py", "test"],
    check=True,
    cwd=repo,
    env={
        **os.environ,
        "VIRTUAL_ENV": "",
        "PATH": path_var,
    },
)

# cookiecutter --output-dir build/ --config-file config_file
