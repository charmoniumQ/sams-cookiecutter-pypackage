# What is this?

This is a [cookiecutter] for creating Python packages.

Usage:

```shell
$ cookiecutter gh:charmoniumQ/sams-cookiecutter-pypackage
package_name: foo-package
author_name: Samuel Grayson
license_spdx [NCSA]: (enter for default)
python_version [^3.8]:
enable_cli [y]:
enable_resource_directory [y]:
...
$ cd foo-package
$ cat TODO.md
```

## Features

- Dependency management ([Poetry]):

  - **Why [Poetry]:** Raw setup.py is unideal, so is requirements.txt. The jury is still out on [Pipenv]
    vs. [Poetry]. I decided to just pick one and see how it would work. Pipenv still requires one to
    write a `setup.py`, so I picked Poetry. Poetry automates the process of deploying as well.

- Everything beyond this point is strictly optional.

- Repository metadata:

  - **README template:** (badges not implemented yet [example badges])

  - **Code of Conduct:** Exact source is specifiable, but [Contributor Covenant] by default; can also be
    skipped.

  - **License:** Downloads license according to the SPDX identifier (also puts this in the SPDX
    identifier in machine-discoverable places).

- Fast dev/test cycle:


  - **Formatting ([autoflake], [isort], [black]):** Linting is a good first step, but autoformatting is
    the logical completion. You rarely have to manually enforce code style with these tools.

  - **Linting ([pylint]):** Linting can go far beyond capturing formatting/style problems. Pylint is
    regarded as the pickiest linter. Pylint also warns of semantic errors often much faster than the
    unittests would have. Pylint has a reputation for being the 'pickiest' linter, so usually big
    projects use [flake8] instead. However, If you are starting a project from scratch, it is easier
    to keep good coding standards from the start. One can also add project-level ignore-rules for
    the overly pedantic stuff.

  - **Static analysis ([mypy], [bandit]):** By default, mypy strict is enabled. Again, maintaining
    strict, static typing from the start is much easier than translating to strict typing. Bandit is
    a new tool I discovered to detect security vulnerabilities (injections, etc.) by analyzing the
    AST. It can be excluded (default) if you do not need security guarantees.

  - **Unittesting ([pytest]):** I follow the separate `tests/` convention.

  - **Code coverage report ([coverage]):** `htmlcov=t ./scripts/test.sh`

- CI/CD:

   - **Pipeline provider:** Github, Travis, or other? (not implemented yet).

  - **[Tox] test env:** can test over a matrix of versions.

  - **Upload code coverage report ([codecov]):** If the token is available (as in CI/CD
    environments), `./scripts/test.sh` will upload to codecov.

- [Sphinx] documentation (`./scripts/docs.sh` and open `docs/_build/index.html`):

  - **Beautiful theme ([Alabaster theme]):** This is easily changeable in the generated project.

  - **[Auto API documentation]:** supports Sphinx, Google-style, and Numpy-style doc-strings
    ([napoleon]). Readers can also glean a lot of information from the types in each function
    signature.

  - **Improved API docs:** [intersphinx], [view code], types in description as well as signature
    (not implemented yet).

  - **[Doctests]:** keep documentation up-to-date automatically.


- Deploy script (`./scripts/deploy.sh`):

  - **Why is this relevant to my project:** Almost every project has a concept of "publishing" or
    "deploying", so this can be overloaded for yours (could be run in CI/CD).

  - **Publish as Python package:** The script can publish to [PyPI], although the repository is
    configurable through `pyproject.toml`.

  - **Publish documentation:** to [GitHub Pages] or [ReadTheDocs] (not implemented yet).

  - **Version bumping ([bump2version]):** Publishing Automatically bumps the
    version. E.g. `./scripts/deploy.sh minor` bumps the minor-version number, making a new commit
    and a new tag for that version.

- Other features:

  - **CLI through [click]:** [Here's][1] a shakedown of the various options for a
      commandline-interface. Click is by far the most concise. It also has facilities for being
      passed an extant file (accepting UNIX conventions like `-`)

  - **Resource directory (`res/`):** This directory and its contents will be present in all package
    installations. Non-python configurations or data could go here.

- TODO:

  - **Namespace packages**

  - **Deduplicate linting**

  - **Make black compatible with autoflake**

  - **Make tests part of package** This way, `mypy -p ${package}` works.

[Pipenv]: https://pipenv.pypa.io/en/latest/
[Poetry]: https://python-poetry.org/
[click]: https://click.palletsprojects.com/
[1]: https://realpython.com/comparing-python-command-line-parsing-libraries-argparse-docopt-click/"
[Contributor Covenant]:  https://www.contributor-covenant.org/
[autoflake]: https://github.com/myint/autoflake
[isort]: https://github.com/timothycrosley/isort
[black]: https://github.com/psf/black
[pylint]: https://pylint.org/
[mypy]: https://mypy.readthedocs.io/en/stable/
[bandit]: https://github.com/PyCQA/bandit
[pytest]: https://docs.pytest.org/en/stable/
[coverage]: https://coverage.readthedocs.io/en/coverage-5.1/
[codecov]: https://codecov.io/
[Alabaster theme]: https://alabaster.readthedocs.io/en/latest/
[bump2version]: https://github.com/c4urself/bump2version/
[example badges]: https://pypi.org/project/inquirer/
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[sphinx]: https://www.sphinx-doc.org/
[tox]: https://tox.readthedocs.io/en/latest/
[Auto API documentation]: https://sphinx-autoapi.readthedocs.io/en/latest/
[napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[intersphinx]: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
[view code]: https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
[doctests]: https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html
[PyPI]: pypi.org/
[GitHub Pages]: https://pages.github.com/
[flake8]: https://flake8.pycqa.org/en/latest/index.html
[ReadTheDocs]: https://readthedocs.org/
