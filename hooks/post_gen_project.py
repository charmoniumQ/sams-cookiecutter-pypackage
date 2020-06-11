import os
import shutil
from pathlib import Path
import urllib

# str() helps mypy not be smart
if str("{{cookiecutter.enable_cli}}") != "y":
    os.remove(Path(".") / "{{cookiecutter.package_name}}" / "cli.py")


if str("{{cookiecutter.enable_resource_directory}}") != "y":
    shutil.rmtree(Path(".") / "res")

if str("{{cookiecutter.enable_codecov}}") == "y":
    with (Path(".") / "TODO.md").open("a") as f:
        f.write(
            """

- [ ] Find your codecov secret (e.g. [for GitHub][1], [in general][2]),
      and put it in your CI/CD environment.

[1]: https://codecov.io/gh/{{cookiecutter.repository_user}}/{{cookiecutter.repository_name}}
[2]: https://docs.codecov.io/docs
"""
        )

try:
    urllib.request.urlopen('https://github.com/spdx/license-list-data/blob/master/text/{{cookiecutter.license_name}}.txt')
except:
    
