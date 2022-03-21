import {{ cookiecutter.package_name }}

def test_main():
    assert {{ cookiecutter.package_name }}.__version__ == "{{ cookiecutter.version }}"
