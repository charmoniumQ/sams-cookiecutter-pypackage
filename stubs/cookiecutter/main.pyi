from typing import Optional, Mapping


def cookiecutter(
        template: str,
        checkout: Optional[str] = None,
        no_input: bool = False,
        extra_context: Optional[Mapping[str, str]] = None,
        replay: bool = False,
        overwrite_if_exists: bool = False,
        output_dir: str = '.',
        config_file: Optional[str] = None,
        default_config: bool = False,
        password: Optional[str] = None,
        directory: Optional[str] = None,
        skip_if_file_exists: bool = False
) -> None:
    ...
