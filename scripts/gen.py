#!/usr/bin/env python

import json

with open("cookiecutter.json") as f:
    option_defaults = json.load(f)

option_options = {option: f"{{cookiecutter.{option}}}" for option in option_defaults}

with open("{{cookiecutter.repository_name}}/cookiecutter_selection.json", "w") as f:
    json.dump(option_options, f, indent=2)
