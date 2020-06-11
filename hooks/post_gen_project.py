import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

# str() helps mypy not be smart about comparing literals
enable_cli = str("{{cookiecutter.enable_cli}}") == "y"
enable_resource_directory = str("{{cookiecutter.enable_resource_directory}}") == "y"
enable_codecov = str("{{cookiecutter.enable_codecov}}") == "y"
repository_user = "{{cookiecutter.repository_user}}"
repository_name = "{{cookiecutter.repository_name}}"
license_name = "{{cookiecutter.license_name}}"
setup_git = str("{{cookiecutter.setup_git}}") == "y"
repository_url = "{{cookiecutter.repository_url}}"
enable_mypy = str("{{cookiecutter.enable_mypy}}") == "y"
enable_pylint = str("{{cookiecutter.enable_pylint}}") == "y"


def add_todo(text: str) -> None:
    with (Path(".") / "TODO.md").open("a") as f:
        f.write(text + "\n")


if not enable_cli:
    os.remove(Path(".") / "{{cookiecutter.package_name}}" / "cli.py")


if not enable_resource_directory:
    shutil.rmtree(Path(".") / "res")


if not enable_mypy:
    os.remove(Path(".") / "mypy.ini")


if not enable_pylint:
    os.remove(Path(".") / ".pylintrc")


if enable_codecov:
    add_todo(
        f"""
- [ ] Find your codecov secret (e.g. [for GitHub][1], [in general][2]),
      and put it in your CI/CD environment.

[1]: https://codecov.io/gh/{repository_user}/{repository_name}
[2]: https://docs.codecov.io/docs
""".lstrip()
    )


if not setup_git:
    add_todo("- [ ] Setup version control system (like Git).")


url = f"https://github.com/spdx/license-list-data/blob/master/text/{license_name.upper()}.txt"
try:
    license_source = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    print(f"Unable to find license {license_name} in [SPDX repository][1].")
    print("[1]: https://github.com/spdx/license-list-data/blob/master/text")
    add_todo("- [ ] Select a license.")
else:
    with (Path(".") / "LICENSE.txt").open("wb") as license_dest:
        license_dest.write(license_source.read())
    add_todo("- [ ] Fill copyright informaiton into license (if necessary).")


if setup_git:
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "remote", "add", "origin", repository_url], check=True)
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(
        ["git", "commit", "-m", "Iniital commit (with sams-cookiecutter-pypackage)"],
        check=True,
    )
    # Allow user to poke around before pushing
