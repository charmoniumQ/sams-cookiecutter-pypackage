# What is this?

This is a [cookiecutter] for creating Python packages.

Usage:

```shell
$ cookiecutter gh:charmoniumQ/sams-cookiecutter-pypackage
<go through prompts>
$ cd package
$ cat TODO.md
```

## Features

- Dependency management ([Poetry])

  - Raw setup.py is unideal, so is requirements.txt. The jury is still
    out on [Pipenv] vs. [Poetry]. I decided to just pick one and
    see how it would work. Pipenv still requires one to write a
    `setup.py`, so I picked Poetry. Poetry automates the process of
    deploying as well.

- Everything beyond this point is strictly optional.

- CLI through [click]

  - [Here's][1] a shakedown of the various options for a
    commandline-interface. Click is by far the most concise. It also
    has facilities for being passed an extant file (accepting UNIX
    conventions like `-`)

- Resource directory which will be present in
  installations. Non-python configurations or data could go here.

- Repository metadata

  - README template (badges not implemented yet [example badges])

  - code of conduct

    - Exact source is specifiable, but [Contributor Covenant] by
      default; can also be skipped.

  - License

    - Downloads license according to the SPDX identifier (also puts
      this in the SPDX identifier in machine-discoverable places).

- Software tools

  - Formatting ([autoflake], [isort], [black])

    - Linting is a good first step, but autoformatting is the logical
      completion. You rarely have to manually enforce code style with
      these tools.

  - Linting ([pylint])

     - Pylint is regarded as the pickiest linter. This is appropriate
       when starting a project from scratch. If you keep good coding
       standards from the start, adhering to them is not that
       difficult. One can also add project-level ignore-rules for the
       overly pedantic stuff, so I don't feel bad about pickin a picky
       linter.

  - Static analysis ([mypy], [bandit])

    - By default, mypy strict is enabled. Again, maintaining strict,
      static typing from the start is much easier than translating to
      strict typing. Bandit is a new tool I discovered to detect
      security vulnerabilities (injections, `eval()`s) by analyzing
      the AST. I will see if it works for me.

  - Unittesting ([pytest])

    - I follow the separate `tests/` convention.

  - Clean tool integration script.

    - Developers just have remember one command for their
      dev-test-cycle `./scrpits/test.sh` which runs auto-formatting,
      linting, static analysis, and unittests. This can be extended
      with named option variables, such as `skip_lint=t
      ./scripts/test.sh`.

  - Local code coverage report ([coverage])

      `htmlcov=t ./scripts/test.sh`

- CI/CD (Github, Travis, other?)

  - Not implemented yet.

  - [Tox] test env, for testing over a matrix of versions.

  - If the token is available (as in CI/CD environments),
    `./scripts/test.sh` will upload to codecov.

- [Sphinx] documentation

  - [Alabaster theme] looks beautiful.

  - Auto API documentation

    - Sphinx, Google-style, and Numpy-style doc-strings are
      supported. Readers can also glean a lot of information from the
      types in each function signature.

  - Improved API docs (intersphinx, view code, types in description as well as signature)

    - Not implemented yet.

  - Doctests keep documentation up-to-date automatically.


- Deploy script

  - Almost every project has a concept of "publishing" or "deploying",
    so this can be overloaded for yours (could be run in CI/CD).

  - Publish to PyPI.

  - Publish documentation to GitHub Pages (not implemented yet).

  - Automatically bumps the version ([bump2version]).

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
