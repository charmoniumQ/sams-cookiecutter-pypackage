import itertools
import io
import csv
import shutil
from pathlib import Path
import urllib.request

license = "MIT"
#license = "{{ cookiecutter.license }}"
#package_name = "{{ cookiecutter.package_name }}"

SPDX_to_trove_url = "https://gist.githubusercontent.com/charmoniumQ/475860168b3d9cb85ffde86deb551141/raw/0bec205fa659c0709e8e266f1fdc6acabc711261/SPDX_to_Trove.csv"
rows = csv.reader(io.StringIO(urllib.request.urlopen(SPDX_to_trove_url).read().decode()))
SPDX_to_trove = dict(itertools.islice(rows, 1, None))
if license in SPDX_to_trove:
    trove_classifier = SPDX_to_trove[license]
    pyproject_file = Path("pyproject.toml")
    pyproject_file.write_text(
        pyproject_file.read_text()
        .replace("# TODO: Insert trove license classifier here.", f'"{trove_classifier}",')
    )
    license_text = urllib.request.urlopen(f"https://spdx.org/licenses/{license}.txt").read()
    Path("LICENSE").write_bytes(license_text + b"\n")
else:
    print(f"Unknown SPDX license identifier {license}")

import sys; sys.exit()

if "." in package_name:
    src_path = Path(package_name)
    dst_path = Path(*package_name.split("."))
    dst_path.mkdir(parents=True, exist_ok=True)
    for path in src_path.iterdir():
        path = path.relative_to(src_path)
        if (dst_path / path).exists():
            (dst_path / path).unlink()
        if (src_path / path).is_dir():
            shutil.copyfiletree(src_path / path, dst_path)
        else:
            shutil.move(src_path / path, dst_path)
    src_path.rmdir()
