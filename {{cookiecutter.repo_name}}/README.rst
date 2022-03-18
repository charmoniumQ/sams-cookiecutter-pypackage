==========================
{{cookiecutter.repo_name}}
==========================

{% if cookiecutter.pypi_package == "yes" -%}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.package_name }}
   :alt: PyPI Package
   :target: https://pypi.org/project/{{ cookiecutter.package_name }}
.. image:: https://img.shields.io/pypi/dm/{{ cookiecutter.package_name }}
   :alt: PyPI Downloads
   :target: https://pypi.org/project/{{ cookiecutter.package_name }}
.. image:: https://img.shields.io/pypi/l/{{ cookiecutter.package_name }}
   :alt: License
   :target: {{ cookiecutter.repo_url }}/blob/main/LICENSE
.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.package_name }}
   :alt: Python Versions
   :target: https://pypi.org/project/{{ cookiecutter.package_name }}
.. image:: https://img.shields.io/librariesio/sourcerank/pypi/{{ cookiecutter.package_name }}
   :alt: libraries.io sourcerank
   :target: https://libraries.io/pypi/{{ cookiecutter.package_name }}
{%- endif %}
{% if 'github' in cookiecutter.repo_url -%}
.. image:: https://img.shields.io/github/stars/{{ cookiecutter.repo_user }}/{{ cookiecutter.repo_name }}?style=social
   :alt: GitHub stars
   :target: {{ cookiecutter.repo_url }}
.. image:: {{ cookiecutter.repo_url }}/actions/workflows/main.yaml/badge.svg
   :alt: CI status
   :target: {{ cookiecutter.repo_url }}/actions/workflows/main.yaml
.. image:: https://img.shields.io/github/last-commit/charmoniumQ/charmonium.determ_hash
   :alt: GitHub last commit
   :target: {{ cookiecutter.repo_url }}/commits
{%- else -%}
.. image:: https://img.shields.io/badge/repo-yes-success
   :alt: Repo
   :target: {{ cookiecutter.repo_url }}
{%- endif %}
.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
   :target: https://mypy.readthedocs.io/en/stable/
   :alt: Checked with Mypy
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: black

{{ cookiecutter.description }}

{% if cookiecutter.pypi_package == "yes" %}
----------
Quickstart
----------

If you don't have ``pip`` installed, see the `pip install
guide`_.

.. _`pip install guide`: https://pip.pypa.io/en/latest/installing/

.. code-block:: console

    $ pip install {{ cookiecutter.repo_name }}

>>> import {{ cookiecutter.package_name }}
{% endif %}
