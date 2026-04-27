"""Insert a one-line link to LESSON.md at the top of each chapter README,
right under the status badge line. Idempotent — re-running adds the link only
if it isn't already present.
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

MARK = '> 📘 **Detailed lesson plan:**'


def patch(p: Path):
    txt = p.read_text(encoding='utf-8')
    if MARK in txt:
        return False
    lines = txt.splitlines()
    # Insert after the status line (the line starting with "> **Status:**")
    out = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if not inserted and ln.startswith('> **Status:**'):
            out.append('')
            out.append(f'{MARK} see [`LESSON.md`](LESSON.md) for the ordered TOC, definitions, theory, notebook cells, and exercises.')
            inserted = True
    if not inserted:
        return False
    p.write_text('\n'.join(out) + '\n', encoding='utf-8')
    return True


def main():
    chapters_dir = ROOT / 'chapters'
    n = 0
    for ch in sorted(chapters_dir.iterdir()):
        readme = ch / 'README.md'
        if readme.exists() and patch(readme):
            print(f'  patched: {readme.relative_to(ROOT)}')
            n += 1
    print(f'\n✓ Patched {n} chapter READMEs.')


if __name__ == '__main__':
    main()
