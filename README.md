# Sam's Cookiecutter repo for Python packages

![GitHub stars](https://img.shields.io/github/stars/charmoniumQ/sams-cookiecutter-pypackage?style=social)
![CI Status](https://github.com/charmoniumQ/sams-cookiecutter-pypackage/actions/workflows/main.yaml/badge.svg)
![Last commit](https://img.shields.io/github/last-commit/charmoniumQ/charmonium.determ_hash)

This is a [cookiecutter] for creating Python packages. See
[charmonium.cache] for an exmaple of a project generated with this
cookiecutter.

## Usage

```shell
$ pip install --user cookiecutter

$ cookiecutter gh:charmoniumQ/sams-cookiecutter-pypackage
# Fill these prompts
repo_name: foo-package
package_name: foo_package
description: foo the bar with a baz
...

$ cd foo_package

# There are mulitple ways to enter the development environment.
# See `CONTRIBUTING.md` in the generated repo.
# I recommend using direnv.
$ direnv allow
# Now you are in the development environment.

# Hackity hack hack.

$ ./script.py fmt
# Autoformats code

$ ./script.py test
# Tests code

$ git push
# (Assuming git was setup)
# Runs CI tests in Github.

$ ./script.py publish minor
# Bumps minor version
# Publishes package to PyPI
# Publishes documentation to Github pages

# If you change your mind on these options, or if I update the cookiecutter, you can regenerate your project like so:
$ $EDITOR cookiecutter_replay.json
# Revise selections

$ cookiecutter gh:charmoniumQ/sams-cookiecutter-pypackage.git \
    --output-dir . \
    --overwrite-if-exists \
    --replay \
    --replay-file cookiecutter_replay.json

# Then go through the differences with `git add -p` or a Git GUI tool.
```

## Features

- `./script.py`: This script has run commands for all of the tools you should
  need. Putting these all into a script gives three advantages:

  - It makes it easier to standardize the which tools are invoked and how they
    are invoked between developers and CI.

  - It lets some of the configuration be dynamic rather than repeated. This
    reduces repetition. For example, `pytest-cov` needs to know what to measure
    coverage against. The script finds the current package and uses that rather
    than repeating the name in many more places.

  - It can run multiple devtools in parallel that would be tedious to type
    out. For example, `./script.py test` runs all six tools in parallel.

- `./script.py fmt`: Fix your code in place

   - [autoimport] guesses and inserts the import statement if you forget to
     write it.

   - [isort] your imports, so you don't have to.

   - [Black] "aims to enforce one style and one style only, with some room for
     pragmatism." If you don't like how this formats a single line, you can
     ignore just that section with `# fmt: off`/`# fmt: on`.

- `./script.py test`: Runs tests on your code.

  - [pylint] is the most thorough and it warns for semantic errors. If some
    particular warning is bothering you, you can ignore it in the
    `pylintrc`. Pylint gives you a colorful report to see if your code has
    worsened.

  - [mypy] type-checks Python code with type annotations. By default, strict
    mode is enabled, but this can be relaxed in `pyproject.toml` >
    `tool.mypy`. It is far easier to use type checking from the beginning than
    it is to enforce type checking on an untyped project.

  - [pytest] runs tests in parallel with debug information. This cookiecutter
    includes a template for writing your own tests.

  - [coverage.py] to evaluate code coverage of the tests.

  - [radon] tells you which modules and functions are most complex. This helps
    you know what to simplify.

- `./script.py all-tests`: Runs extra tests on your code in every environment.

  - [tox] runs tests in multiple Python environments, so you can test
    compatibility.

  - [rstcheck] and [proselint] checks your `README.rst`.

  - [twine] checks the resulting package.

- `./script.py publish`: Publishes the code to PyPI and documentation to Github pages.
  - [bump2version] bumps the version, writes a git tag, and pushes it to Github
    (if everything succeeded).

  - [poetry] does the actual build and publish. Set `TWINE_USERNAME` and
    `TWINE_PASSWORD` to automate entering credentials.

- `./script.py docs`: Check and render documentation.

  - [proselint] checks grammar and spelling in ReStructured Text files.

  - TODO: generate API docs. I am unhappy with sphinx and looking for
    replacements.

- Github workflow automation: Creates a basic automation workflow that runs
  `./script.py all-tests`.

- A minimal but useful Github issue template.

- A note on packages: Even if you don't intend to publish a package, you should
  probably think of your code as a package, because this gives you a single
  namespace to put your modules, most dependency tools operate at the
  package-level, and `pyproject.toml` operates at a package-level.

- `README.rst` with cool-looking automatic status buttons. The ReStructured Text
  is a bit less pleasant than Markdown, but Markdown is still a second-class
  citizen on PyPI, whereas both can render ReStructuredText just
  fine. `rstcheck` should help the syntax issues.

- `pyproject.toml` introduced in [PEP 518] is the replacement for `setup.py` and
  `setup.cfg`. It is a unified space for storing the configuration of arbitrary
  tools.

- (Optional) [Poetry] for dependency management: Poetry is a tool for managing
  the lifecycle of Python packages. It replaces the verbose `setup.py` and
  `setup.cfg`. Should you want to publish your package, Poetry makes that easy,
  unlike [Pipenv].

- (Optional) [Nix] for package management: If you need system-level dependencies
  (e.g. C libraries, Python versions), Nix can install these for you. If you
  already have a system that works, you can safely ignore `flake.nix`. If you
  use this, it guarantees you have the exact same development environment as CI
  and other developers. Even if you already have a satisfactory system python,
  consider using Nix because it builds multiple isolated Pythons for use with
  Tox.

- [Contributor Covenant] as the Code of Conduct. If you are philosophically
  opposed to codes of conduct, just remove it in the generated repo.

# Documentation

- `repo_name`: Repository name in Github and on PyPI.

- `package_name`: Importable package name (must be a valid Python identifier).

- `description`: One sentence or phrase describing the package's purpose.

- `license`: [SPDX license identifier] like `MIT` or `GPL-3.0-only`.

- `repo_user`: If on Github, your Github username. Otherwise, this doesn't
  matter

- `repo_url`: The URL at which the code repo is accessible.

- `version`: Initial version.

- `use_poetry`: Whether to use poetry for dependency management.

- `pypi_package`: Whether to set up publishing on [PyPI] (doesn't publish
  anything until you run `./script.py publish`). This requires use of poetry.

- `keywords`: If publishing to PyPI, put relevant keywords to make your package
  discoverable.

- `trove_license`: If publishing to PyPI, copy zero or more `License ::`
  identifier from [PyPI classifiers].

- `trove_intended_audience`: If publishing to PyPI, copy zero or more
  comma-separated `Intended Audience ::` identifiers from [PyPI classifiers].

- `trove_topics`: If publishing to PyPI, copy zero or more comma-separated
  `Topic ::` identifiers from [PyPI classifiers].

- `trove_other_classifiers`: If publishing to PyPI, copy **zero or more**
  comma-separated identifiers from [PyPI classifiers].

# TODO

- [x] Add doctests to Pytest.
- [x] Add bump2version.
- [x] Add Tox to test multiple Python versions.
- [x] Add Nix to install multiple Python versions.
- [x] Use `envrc` to activate environment.
- [x] Support non-GitHub repos.
- [x] Add badges to README.
- [x] Include Trove classifiers.
- [x] Automate handling PyPI credentials.
- [ ] Test this cookiecutter in CI.
  - `./script.py {fmt,test,all-tests}` should work.
  - Should not create any new files.
- [ ] Handle namespace packages better
- [ ] Generate API documentation and push to Github pages.
- [x] Use cookiecutter for this repo.
- [ ] Switch from ReStructured Text to Markdown.
- [ ] Fix {autoimport and removestar and unimport} or pyflyby.
- [ ] Add vulture.


[Pipenv]: https://pipenv.pypa.io/en/latest/
[Poetry]: https://python-poetry.org/
[Contributor Covenant]:  https://www.contributor-covenant.org/
[isort]: https://github.com/timothycrosley/isort
[black]: https://github.com/psf/black
[pylint]: https://pylint.org/
[mypy]: https://mypy.readthedocs.io/en/stable/
[pytest]: https://docs.pytest.org/en/stable/
[coverage.py]: https://coverage.readthedocs.io/en/coverage-5.1/
[bump2version]: https://github.com/c4urself/bump2version/
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[tox]: https://tox.readthedocs.io/en/latest/
[PyPI]: pypi.org/
[radon]: https://radon.readthedocs.io/en/latest/
[PEP 518]: https://peps.python.org/pep-0518/
[rstcheck]: https://github.com/myint/rstcheck
[twine]: https://twine.readthedocs.io/en/latest/
[PyPI classifiers]: https://pypi.org/classifiers/
[Nix]: https://nixos.org/
[SPDX license identifier]: https://spdx.org/licenses/
[charmonium.cache]: https://github.com/charmoniumQ/charmonium.cache/
[autoimport]: https://lyz-code.github.io/autoimport/
[proselint]: http://proselint.com/
