from pathlib import Path
import json

defaults = json.loads(Path("cookiecutter.json").read_text())
replay_file = "cookiecutter_replay.json"
config = {
    "cookiecutter": {
        key: "{{cookiecutter.%s}}" % key
        for key in defaults.keys()
    },
    "comment": f"This repository was created from a template in <https://github.com/charmoniumQ/sams-cookiecutter-pypackage.git> with these options. Use `cookiecutter gh:charmoniumQ/sams-cookiecutter-pypackage.git --output-dir . --overwrite-if-exists --replay --replay-file {replay_file}` to regenerate.",
}
(Path("{{cookiecutter.repo_name}}") / replay_file).write_text(json.dumps(config, indent=2))
