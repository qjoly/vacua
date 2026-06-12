"""Generate a .scad plate for a phrase (multi-line grid possible).

Usage: python scad/generators/plate.py "TWO LINES" out/plate.scad [cols]
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from vacua.scad_emit import write_scad  # noqa: E402


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: plate.py TEXT out.scad [cols]", file=sys.stderr)
        return 2
    text = sys.argv[1].replace(" ", "")  # SCAD ignores spaces
    out = Path(sys.argv[2])
    cols = int(sys.argv[3]) if len(sys.argv) >= 4 else 0
    rel = Path("vacua_param.scad")
    write_scad(text, out, param_path=str(rel), with_keyring=False, merged=True, cols_tiles=cols)
    print(f"Plate generated: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
