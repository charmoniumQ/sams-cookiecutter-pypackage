import {{ cookiecutter.package_name }}


def test_main() -> None:
    assert {{ cookiecutter.package_name }}.__version__ == "{{ cookiecutter.version }}"
