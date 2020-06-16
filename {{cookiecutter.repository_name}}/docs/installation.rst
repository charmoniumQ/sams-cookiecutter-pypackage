.. highlight:: shell

============
Installation
============


Stable release
--------------

To install {{cookiecutter.pypi_name}}, run this command in your terminal:

.. code-block:: console

    $ pip install {{cookiecutter.pypi_name}}

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Dev build
---------

The sources for {{cookiecutter.pypi_name}} can be downloaded from the `Github repo`_.

These sources can be installed with `Poetry`_

.. code-block:: console

    $ git clone {{cookiecutter.repository_url}}
    $ cd {{cookiecutter.repository_name}}
    $ pip install poetry
    $ poetry install

.. _Github repo: {{cookiecutter.repository_url}}
.. _Poetry: https://python-poetry.org/
