"""Generate LESSON_PLANS.docx from LESSON_PLANS.md.

Hand-rolled markdown converter targeting the specific patterns used in the
master file:
  ## Chapter N — ...        → H1 (page-break before)
  ### Section name           → H2
  **Reading:** N · ...       → metadata block
  N.M **[TYPE]** body        → typed TOC item (colored badge + body)
  - / * bullet               → bulleted list
  1. text                    → numbered list
  Inline: **bold**, *italic*, `code`
  ---                        → horizontal rule

Usage: python generate_lesson_plans_docx.py
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


ROOT = Path(__file__).parent.resolve()
SRC = ROOT / 'LESSON_PLANS.md'
OUT = ROOT / 'LESSON_PLANS.docx'

# Colors
NAVY = RGBColor(0x1F, 0x3A, 0x68)
DARK = RGBColor(0x22, 0x22, 0x22)
GRAY = RGBColor(0x55, 0x55, 0x55)
LIGHT_GRAY = RGBColor(0x88, 0x88, 0x88)

# Section type → badge color
TYPE_COLORS = {
    'HOOK':    RGBColor(0xC7, 0x64, 0x2A),  # orange
    'DEF':     RGBColor(0x2D, 0x7A, 0x3E),  # green
    'CONCEPT': RGBColor(0x1F, 0x3A, 0x68),  # navy
    'THEORY':  RGBColor(0x6A, 0x1B, 0x9A),  # purple
    'CODE':    RGBColor(0x2E, 0x2E, 0x2E),  # near-black
    'NB':      RGBColor(0x00, 0x66, 0x99),  # blue
    'FIG':     RGBColor(0xC2, 0x1A, 0x6B),  # magenta
    'PROD':    RGBColor(0x99, 0x55, 0x00),  # brown
    'EX':      RGBColor(0xB0, 0x2B, 0x2B),  # red
    'READ':    RGBColor(0x55, 0x55, 0x55),  # gray
}


# ---------- inline parsing ----------

INLINE_RE = re.compile(
    r'(\*\*[^*]+\*\*)'      # **bold**
    r'|(\*[^*\n]+\*)'        # *italic*
    r'|(`[^`]+`)'            # `code`
)

def add_inline(paragraph, text, base_size=11, base_color=DARK, base_bold=False):
    """Add a string with **bold**, *italic*, `code` parsed into separate runs."""
    # Replace HTML-ish entities and common UTF chars
    text = text.replace('&nbsp;', ' ')

    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            r = paragraph.add_run(text[pos:m.start()])
            r.font.size = Pt(base_size)
            r.font.color.rgb = base_color
            r.font.bold = base_bold
        if m.group(1):  # **bold**
            r = paragraph.add_run(m.group(1)[2:-2])
            r.font.size = Pt(base_size)
            r.font.color.rgb = base_color
            r.font.bold = True
        elif m.group(2):  # *italic*
            r = paragraph.add_run(m.group(2)[1:-1])
            r.font.size = Pt(base_size)
            r.font.color.rgb = base_color
            r.font.italic = True
        elif m.group(3):  # `code`
            r = paragraph.add_run(m.group(3)[1:-1])
            r.font.size = Pt(base_size - 1)
            r.font.name = 'Consolas'
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        pos = m.end()
    if pos < len(text):
        r = paragraph.add_run(text[pos:])
        r.font.size = Pt(base_size)
        r.font.color.rgb = base_color
        r.font.bold = base_bold


def add_horizontal_line(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'AAAAAA')
    pBdr.append(bottom)
    pPr.append(pBdr)


# ---------- TOC item parsing ----------

TOC_RE = re.compile(r'^(\d+\.\d+)\s+\*\*\[([A-Z\-]+)\]\*\*\s+(.*)$')


def add_toc_item(doc, line):
    """Render a 'N.M **[TYPE]** body' line as a styled paragraph."""
    m = TOC_RE.match(line)
    if not m:
        # Fallback: regular paragraph with inline parsing
        p = doc.add_paragraph()
        add_inline(p, line)
        return

    num, tag, body = m.group(1), m.group(2), m.group(3)
    color = TYPE_COLORS.get(tag, GRAY)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.4)

    # Number
    r = p.add_run(num + ' ')
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = LIGHT_GRAY

    # [TYPE] badge
    r = p.add_run(f'[{tag}]')
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = color
    r.font.name = 'Consolas'

    # Body
    p.add_run(' ')
    add_inline(p, body)


# ---------- block-level renderer ----------

def render(doc, lines):
    """Walk lines and emit paragraphs."""
    i = 0
    in_list_numbered = False
    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        # Page break + heading 1: chapter
        if line.startswith('## Chapter '):
            # Chapter heading on a new page
            p_break = doc.add_paragraph()
            p_break.add_run().add_break(WD_BREAK.PAGE)

            text = line[3:]  # strip "## "
            h = doc.add_heading('', level=1)
            h.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = h.add_run(text)
            r.font.size = Pt(20)
            r.font.bold = True
            r.font.color.rgb = NAVY
            add_horizontal_line(h)
            i += 1
            continue

        # Other H2 (e.g., "## How to use these lesson plans")
        if line.startswith('## '):
            h = doc.add_heading('', level=1)
            r = h.add_run(line[3:])
            r.font.size = Pt(18)
            r.font.bold = True
            r.font.color.rgb = NAVY
            i += 1
            continue

        # H3 — Detailed TOC / Notebook cells / Glossary / References
        if line.startswith('### '):
            h = doc.add_heading('', level=2)
            r = h.add_run(line[4:])
            r.font.size = Pt(13)
            r.font.bold = True
            r.font.color.rgb = NAVY
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
            i += 1
            continue

        # H1 (only the doc title at top)
        if line.startswith('# '):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(line[2:])
            r.font.size = Pt(24)
            r.font.bold = True
            r.font.color.rgb = NAVY
            i += 1
            continue

        # Horizontal rule
        if stripped == '---':
            p = doc.add_paragraph()
            add_horizontal_line(p)
            i += 1
            continue

        # Bulleted list (-/*)
        if stripped.startswith('- ') or stripped.startswith('* '):
            content = stripped[2:]
            p = doc.add_paragraph(style='List Bullet')
            add_inline(p, content)
            i += 1
            continue

        # Numbered list "1. text"
        if re.match(r'^\d+\.\s', stripped):
            content = re.sub(r'^\d+\.\s+', '', stripped)
            p = doc.add_paragraph(style='List Number')
            add_inline(p, content)
            i += 1
            continue

        # Blockquote
        if line.startswith('> '):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.6)
            r = p.add_run('▎ ')
            r.font.bold = True
            r.font.color.rgb = NAVY
            add_inline(p, line[2:], base_color=GRAY)
            i += 1
            continue

        # HTML comment block
        if stripped.startswith('<!--'):
            while i < len(lines) and '-->' not in lines[i]:
                i += 1
            i += 1
            continue

        # Empty line
        if not stripped:
            i += 1
            continue

        # TOC item: "N.M **[TYPE]** ..."
        if TOC_RE.match(stripped):
            add_toc_item(doc, stripped)
            i += 1
            continue

        # Regular paragraph (handles **Reading:**, **Prereqs:**, etc.)
        p = doc.add_paragraph()
        add_inline(p, stripped)
        i += 1


# ---------- main ----------

def main():
    if not SRC.exists():
        print(f'ERROR: {SRC} not found.')
        sys.exit(1)

    text = SRC.read_text(encoding='utf-8')
    lines = text.splitlines()

    doc = Document()

    # Default style
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # Cover
    cover_title = doc.add_paragraph()
    cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cover_title.add_run('Detailed Lesson Plans')
    r.font.size = Pt(34)
    r.font.bold = True
    r.font.color.rgb = NAVY

    cover_sub = doc.add_paragraph()
    cover_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cover_sub.add_run('Computer Vision: From Foundations to Frontier (2026)')
    r.font.size = Pt(18)
    r.font.italic = True
    r.font.color.rgb = GRAY

    cover_sub2 = doc.add_paragraph()
    cover_sub2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cover_sub2.add_run('Per-chapter ordered TOCs — definitions → concepts → theory → code → notebook cells')
    r.font.size = Pt(12)
    r.font.color.rgb = GRAY
    cover_sub2.paragraph_format.space_after = Pt(40)

    # Author & meta
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for label, val, bold in [
        ('Author', 'Milan Amrut Joshi', True),
        ('Repo', 'github.com/mlnjsh/computer-vision-book', False),
        ('Companion', 'BOOK_OUTLINE.docx · WRITING_PLAN.xlsx · LESSON_PLANS.md', False),
    ]:
        r = meta.add_run(f'\n{label}: ')
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = DARK
        r2 = meta.add_run(val)
        r2.font.size = Pt(11)
        r2.font.color.rgb = DARK
        if bold:
            r2.font.bold = True

    doc.add_paragraph()
    legend = doc.add_paragraph()
    legend.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = legend.add_run('Section type legend')
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = NAVY

    legend2 = doc.add_paragraph()
    legend2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    legend2.paragraph_format.space_after = Pt(6)
    legend_items = [
        ('HOOK',    'motivating story'),
        ('DEF',     'definitions'),
        ('CONCEPT', 'intuition'),
        ('THEORY',  'math'),
        ('CODE',    'inline snippet'),
        ('NB',      'notebook cell'),
        ('FIG',     'figure'),
        ('PROD',    'production note'),
        ('EX',      'exercise'),
        ('READ',    'external reading'),
    ]
    for tag, desc in legend_items:
        r = legend2.add_run(f'[{tag}] ')
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.name = 'Consolas'
        r.font.color.rgb = TYPE_COLORS[tag]
        r2 = legend2.add_run(f'{desc}    ')
        r2.font.size = Pt(10)
        r2.font.color.rgb = GRAY

    # Skip the master's first three lines (title + intro paragraphs) — already on cover
    # Find first chapter to start rendering from
    start = 0
    for idx, ln in enumerate(lines):
        if ln.startswith('## Chapter 1'):
            start = idx
            break

    # Render the rest
    render(doc, lines[start:])

    doc.save(OUT)
    print(f'Wrote {OUT}')


if __name__ == '__main__':
    main()
