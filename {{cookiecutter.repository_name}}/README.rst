.. highlight:: python

{% for _ in cookiecutter.repository_name %}={% endfor %}
{{cookiecutter.repository_name}}
{% for _ in cookiecutter.repository_name %}={% endfor %}

{{cookiecutter.description}}


Quickstart
----------

.. code-block:: console

    $ pip install {{cookiecutter.repository_name}}

>>> import {{cookiecutter.package_name}}
>>> {{cookiecutter.package_name}}.returns_four()
4
