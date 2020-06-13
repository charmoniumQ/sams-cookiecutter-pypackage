import click

from .lib import returns_four


@click.command()
def main() -> None:
    """CLI for {{cookiecutter.package_name}}."""
    print(returns_four())
