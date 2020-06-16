{% for _ in cookiecutter.pypi_name %}={% endfor %}
{{cookiecutter.pypi_name}}
{% for _ in cookiecutter.pypi_name %}={% endfor %}

{{cookiecutter.description}}


Quickstart
----------

.. code-block:: console

    $ pip install {{cookiecutter.repository_name}}

.. highlight:: python

>>> import {{cookiecutter.package_name}}
>>> {{cookiecutter.package_name}}.returns_four()
4
