import shutil
from pathlib import Path
import urllib.request

license = "{{ cookiecutter.license }}"
package_name = "{{ cookiecutter.package_name }}"

license_text = urllib.request.urlopen(f"https://spdx.org/licenses/{license}.txt").read()

Path("LICENSE").write_bytes(license_text)

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
