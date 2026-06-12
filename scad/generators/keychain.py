"""Generate a keychain .scad for a short word.

Usage: python scad/generators/keychain.py NAME out/name.scad
"""

from __future__ import annotations

import sys
from pathlib import Path

# Reuse the Python wrapper that drives vacua_param.scad.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from vacua.scad_emit import write_scad  # noqa: E402


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: keychain.py TEXT out.scad", file=sys.stderr)
        return 2
    text = sys.argv[1]
    out = Path(sys.argv[2])
    # The generated wrapper includes ../scad/vacua_param.scad from the output folder.
    # When generating inside the repo, adapt the relative path.
    rel = Path("..") / "scad" / "vacua_param.scad"
    try:
        rel = Path("vacua_param.scad")  # same folder
    except Exception:
        pass
    write_scad(text, out, param_path=str(rel), with_keyring=True, merged=True, cols_tiles=0)
    print(f"Keychain generated: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
