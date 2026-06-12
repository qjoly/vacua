"""Command-line interface for Vacua.

Examples:
    python -m vacua "HELLO" --weight bold --out specimen.png
    python -m vacua --chart --out chart.png
    python -m vacua "AB" --ligature --rotate B --out ligature.png
    python -m vacua "VACUA" --scad --out vacua.scad
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render import compose_rotation_ligature, render_chart, render_paired_text, render_text
from .variants import MODES, WEIGHTS, style_for


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="vacua", description="Vacua font — image and 3D rendering.")
    p.add_argument("text", nargs="?", help="Text to compose (A-Z and ?). Ignored if --chart.")
    p.add_argument("--out", "-o", type=Path, default=Path("vacua.png"), help="Output file.")
    p.add_argument("--weight", "-w", choices=sorted(WEIGHTS.keys()), default="medium",
                   help="Font weight.")
    p.add_argument("--mode", "-m", choices=["spaced", "joined", "solid"], default=None,
                   help="Column mode (overrides the one bundled with the weight).")
    p.add_argument("--no-puce", action="store_true", help="Disable the letter-start marker.")
    p.add_argument("--chart", action="store_true", help="Generate the A-Z chart (ignores `text`).")
    p.add_argument("--ligature", action="store_true",
                   help="Compose a rotation ligature: the 1st letter vertical, --rotate horizontal.")
    p.add_argument("--rotate", type=str, default=None, help="Letter to overlay rotated 90° (--ligature mode).")
    p.add_argument("--pairs", action="store_true",
                   help="Render the text as PAIRS of overlaid letters (2nd rotated 90°). E.g. CAFE → [CA][FE].")
    p.add_argument("--mono", action="store_true",
                   help="(--pairs/--ligature) Force the same color for both letters instead of two-tone.")
    p.add_argument("--scad", action="store_true",
                   help="Instead of an image, write an OpenSCAD file driven by the parametric generator.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    style = style_for(args.weight, args.mode)
    if args.no_puce:
        from dataclasses import replace as _replace
        style = _replace(style, puce=False)

    if args.scad:
        if not args.text:
            print("Error: --scad requires a text.", file=sys.stderr)
            return 2
        from .scad_emit import write_scad
        write_scad(args.text, args.out)
        print(f"OpenSCAD written to {args.out}")
        return 0

    if args.chart:
        img = render_chart(style=style)
    elif args.pairs:
        if not args.text:
            print("Error: --pairs requires a text.", file=sys.stderr)
            return 2
        img = render_paired_text(args.text, style=style, mono=args.mono)
    elif args.ligature:
        if not args.text or len(args.text) < 1 or not args.rotate:
            print("Error: --ligature requires a text (1 vertical letter) and --rotate <letter>.",
                  file=sys.stderr)
            return 2
        color_rot = style.color if args.mono else None
        kwargs = {"color_rotated": color_rot} if color_rot is not None else {}
        img = compose_rotation_ligature(args.text[0], args.rotate[0], style=style, **kwargs)
    else:
        if not args.text:
            print("Error: provide a text or use --chart.", file=sys.stderr)
            return 2
        img = render_text(args.text, style=style)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out)
    print(f"Image written to {args.out}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
