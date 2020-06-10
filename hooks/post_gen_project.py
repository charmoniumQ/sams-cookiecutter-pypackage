import os
from pathlib import Path


if not {{ cookiecutter.enable_cli }}:
    os.remove(Path('.') / "{{cookiecutter.pckage_name}}" / "cli.py")


if not {{ cookiecutter.enable_resource_directory }}:
    shutil.rmtree(Path('.') / "res")
