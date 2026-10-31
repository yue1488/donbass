"""Regenerate every generated file from tools/content.py and validate the result.
Run from anywhere:  python tools/regenerate_all.py   (needs Pillow for the textures)"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for script in ("gen_textures.py", "gen_resources.py", "gen_worldgen.py", "gen_structures.py", "validate.py"):
    print(f"== {script}")
    result = subprocess.run([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    if result.returncode:
        sys.exit(result.returncode)
