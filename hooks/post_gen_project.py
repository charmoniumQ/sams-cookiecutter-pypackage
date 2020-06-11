import shutil
import os
from pathlib import Path


# str() helps mypy not be smart
if str('{{ cookiecutter.enable_cli }}') != 'y':
    os.remove(Path('.') / "{{cookiecutter.package_name}}" / "cli.py")


if str('{{ cookiecutter.enable_resource_directory }}') != 'y':
    shutil.rmtree(Path('.') / "res")
