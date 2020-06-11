if (
    str("{{cookiecutter.enable_codecov}}") == "y"
    or str("{{cookiecutter.enable_coverage}}") == "y"
):
    assert (
        str("{{cookiecutter.enable_pytest}}") == "y"
    ), "If codecov or coverage is enabled, pytest must also be enabled."
