from typing import Union
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
license_spdx = "{{cookiecutter.license_spdx}}"
initial_commit = str("{{cookiecutter.initial_commit}}") == "y"
repository_url = "{{cookiecutter.repository_url}}"
enable_mypy = str("{{cookiecutter.enable_mypy}}") == "y"
enable_pylint = str("{{cookiecutter.enable_pylint}}") == "y"
enable_sphinx = str("{{cookiecutter.enable_sphinx}}") == "y"
code_of_conduct = str("{{cookiecutter.code_of_conduct}}")
enable_bump2version = str("{{cookiecutter.enable_bump2version}}") == "y"


def add_todo(text: str) -> None:
    with open("TODO.md", "a") as f:
        f.write(text + "\n")


if not enable_cli:
    os.remove("{{cookiecutter.package_name}}/_cli.py")


if not enable_resource_directory:
    shutil.rmtree("res")


if not enable_mypy:
    os.remove("mypy.ini")


if not enable_pylint:
    os.remove(".pylintrc")


if enable_codecov:
    add_todo(
        f"""
- [ ] Find your codecov secret (e.g. [for GitHub][1], [in general][2]),
      and put it in your CI/CD environment.

[1]: https://codecov.io/gh/{repository_user}/{repository_name}
[2]: https://docs.codecov.io/docs
""".lstrip()
    )


if not enable_sphinx:
    shutil.rmtree("docs/")
    os.remove("scripts/docs.sh")


if not enable_bump2version:
    os.remove(".bumpversion.cfg")


def download_url(url: str, dest: Union[Path, str, bytes]) -> None:
    text = urllib.request.urlopen(url)
    with open(dest, "wb") as file_dest:
        file_dest.write(text.read())


license_url = f"https://github.com/spdx/license-list-data/blob/master/text/{license_spdx.upper()}.txt"
try:
    download_url(license_url, "LICENSE.txt")
except urllib.error.HTTPError:
    print(f"Unable to find license {license_spdx} in [SPDX repository][1].")
    print("[1]: https://github.com/spdx/license-list-data/blob/master/text")
    add_todo(f"- [ ] Download {license_spdx} license.")
else:
    add_todo("- [ ] Fill copyright informaiton into license (if necessary).")


code_of_conduct_url = {
    "contributor-covenant": "https://www.contributor-covenant.org/version/2/0/code_of_conduct/code_of_conduct.md"
}.get(code_of_conduct, code_of_conduct)

if code_of_conduct_url.startswith("http"):
    download_url(code_of_conduct_url, "CODE_OF_CONDUCT")
    add_todo(
        f"- [ ] Review CODE_OF_CONDUCT ({code_of_conduct}), especially enforcement."
    )
else:
    if code_of_conduct.lower() != "none":
        add_todo(f"- [ ] Add CODE_OF_CONDUCT ({code_of_conduct}).")


if initial_commit:
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(
        ["git", "remote", "add", "origin", repository_url],
        check=True,
        capture_output=True,
    )
    subprocess.run(["git", "add", "-A"], check=True, capture_output=True)
    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            """
Iniital commit (with [sams-cookiecutter-pypackage])

[1]: https://github.com/charmoniumQ/sams-cookiecutter-pypackage
""".lstrip(),
        ],
        check=True,
        capture_output=True,
    )
    # Allow user to poke around before pushing
