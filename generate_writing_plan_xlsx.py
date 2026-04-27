"""Generate the 8-week writing plan as an Excel workbook with multiple sheets."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, FormulaRule


# Colors
BLUE = '1F3A68'
LIGHT_BLUE = 'E8EEF7'
GREEN = '2D7A3E'
LIGHT_GREEN = 'E5F4E8'
ORANGE = 'C7642A'
LIGHT_ORANGE = 'FCEEDC'
GRAY = '4A4A4A'
LIGHT_GRAY = 'F2F2F2'
WHITE = 'FFFFFF'

START_DATE = date(2026, 4, 27)  # next Monday-ish from current date 2026-04-27

CHAPTERS = [
    # (chapter_no, title, target_words, difficulty 1-5, hands_on)
    (1,  "The 2026 Computer Vision Landscape",                    2800, 1, "Mental-model diagram + framework benchmark"),
    (2,  "Image Fundamentals and Pixel-Level Operations",          3000, 1, "Document-cleanup preprocessor (OpenCV)"),
    (3,  "Classical Feature Engineering: SIFT, ORB, Geometry",     3000, 2, "Multi-image panorama + logo detector"),
    (4,  "Camera Geometry, Calibration, and Stereo Vision",        3200, 3, "Webcam calibration + StereoSGBM depth map"),
    (5,  "CNNs: From LeNet to ConvNeXt",                           3200, 2, "ResNet-18 from scratch on CIFAR-10"),
    (6,  "Training Modern Vision Models in Practice",              3000, 2, "Beat a timm baseline with training tricks"),
    (7,  "Object Detection: R-CNN to YOLO26 and DETR",             3300, 3, "YOLO26 vs RT-DETR on Roboflow dataset"),
    (8,  "Image Segmentation: U-Net to SAM 3 + Grounding DINO",    3200, 3, "Zero-shot Gradio segmentation app"),
    (9,  "Vision Transformers and Hybrid Architectures",           3200, 4, "ViT vs ResNet attention/CAM comparison"),
    (10, "Self-Supervised Vision: SimCLR to DINOv3",               3000, 4, "Frozen DINOv3 backbone for downstream seg"),
    (11, "CLIP and Vision-Language Pretraining",                   2800, 3, "CLIP + FAISS photo search app"),
    (12, "Generative Vision: GANs, VAEs, Diffusion Era",           3500, 5, "SDXL LoRA fine-tune + ControlNet chain"),
    (13, "Vision-Language Models: The Multimodal Stack",           3200, 3, "Claude Vision + Qwen2.5-VL doc Q&A"),
    (14, "Document AI and Visual Agents",                          2800, 3, "Invoice extraction + browser-control agent"),
    (15, "Video Understanding: Action, Tracking, VideoMAE",        3000, 4, "Sports-analytics pipeline (detect+track+count)"),
    (16, "3D Vision: Depth, NeRF, Gaussian Splatting",             3200, 5, "Phone-capture to 3DGS fly-through"),
    (17, "Vision-Language-Action Models for Robotics",             3300, 5, "OpenVLA simulation + attention viz"),
    (18, "Domain-Specific Vision: Medical, AV, Geospatial, Agri",  3000, 3, "MONAI chest-X-ray + BEV toy example"),
    (19, "Optimization and Edge Deployment",                       2800, 4, "YOLO26 INT8 → TensorRT → Jetson Orin Nano"),
    (20, "MLOps, Responsible AI, and the Future of CV",            3000, 3, "End-to-end production capstone"),
]

# Chapter-week assignment (8-week plan, parallelized)
WEEK_PLAN = {
    1: [1, 2],
    2: [3, 4],
    3: [5, 6],
    4: [7, 8],
    5: [9, 10],
    6: [11, 12, 13],
    7: [14, 15, 16],
    8: [17, 18, 19, 20],
}

# Detailed daily plan: (week, day_of_week 0=Mon..5=Sat, chapter, activity, hours)
DAILY_PLAN = []

def add_day(week, dow, chapter, activity, hours):
    DAILY_PLAN.append((week, dow, chapter, activity, hours))

# Week 0 — Pre-launch
WEEK0 = [
    (0, 0, None, "Set up GitHub repo: chapters/, notebooks/, figures/, case-studies/", 2),
    (0, 1, None, "Pick running case-study dataset (Roboflow 100 + EY domain)", 2),
    (0, 2, None, "Draft chapter template (intro→theory→code→production→exercises→refs)", 2),
    (0, 3, None, "Block daily writing window on calendar; install reference manager", 1),
    (0, 4, None, "Read MIT visionbook + Stanford CS231n 2026 syllabus", 3),
    (0, 5, None, "Snapshot dependency lockfile (requirements.txt, conda env)", 2),
]
DAILY_PLAN.extend(WEEK0)

# Week 1: Ch 1 (Mon-Wed), Ch 2 (Thu-Sat)
add_day(1, 0, 1, "Ch1: outline + draft sections 1-3 (history, eras, pipeline)", 3)
add_day(1, 1, 1, "Ch1: draft sections 4-6 + framework comparison table", 3)
add_day(1, 2, 1, "Ch1: case-study introduction + figures + edit pass", 3)
add_day(1, 3, 2, "Ch2: draft pixel/color spaces + convolution sections", 3)
add_day(1, 4, 2, "Ch2: edge detection + morphology + thresholding", 3)
add_day(1, 5, 2, "Ch2: document-cleanup preprocessor notebook + edit", 3)

# Week 2: Ch 3 (Mon-Wed), Ch 4 (Thu-Sat)
add_day(2, 0, 3, "Ch3: SIFT/ORB/BRIEF descriptors + matching theory", 3)
add_day(2, 1, 3, "Ch3: RANSAC + homography + Hough transforms", 3)
add_day(2, 2, 3, "Ch3: panorama + logo detector notebook", 3)
add_day(2, 3, 4, "Ch4: pinhole/fisheye models + intrinsics/extrinsics math", 3)
add_day(2, 4, 4, "Ch4: calibration + epipolar geometry + figures", 3)
add_day(2, 5, 4, "Ch4: webcam calibration + StereoSGBM notebook", 3)

# Week 3: Ch 5 (Mon-Wed), Ch 6 (Thu-Sat)
add_day(3, 0, 5, "Ch5: implement ResNet-18 from scratch first, then write around it", 3)
add_day(3, 1, 5, "Ch5: CNN family-tree narrative (LeNet→ConvNeXt)", 3)
add_day(3, 2, 5, "Ch5: CIFAR-10 reproduction + edit + figures", 3)
add_day(3, 3, 6, "Ch6: data loaders + Albumentations + mixup/cutmix", 3)
add_day(3, 4, 6, "Ch6: optimizers + schedulers + AMP + Lightning", 3)
add_day(3, 5, 6, "Ch6: timm baseline-beating notebook + W&B integration", 3)

# Week 4: Ch 7 (Mon-Wed), Ch 8 (Thu-Sat) + mid-book pass
add_day(4, 0, 7, "Ch7: two-stage detectors narrative (R-CNN family)", 3)
add_day(4, 1, 7, "Ch7: YOLO evolution + DETR/RT-DETR + mAP/IoU", 3)
add_day(4, 2, 7, "Ch7: YOLO26 vs RT-DETR benchmark notebook", 3)
add_day(4, 3, 8, "Ch8: U-Net/DeepLab/Mask R-CNN narrative", 3)
add_day(4, 4, 8, "Ch8: SAM 3 + Grounding DINO architecture deep-dive", 3)
add_day(4, 5, 8, "Ch8: Gradio app + mid-book consistency pass", 4)

# Week 5: Ch 9 (Mon-Wed), Ch 10 (Thu-Sat)
add_day(5, 0, 9, "Ch9: attention from scratch + ViT walkthrough", 3)
add_day(5, 1, 9, "Ch9: Swin/MaxViT/Mamba-Vision + when ViT wins/loses", 3)
add_day(5, 2, 9, "Ch9: ViT-Small ImageNette + attention-map figures", 3)
add_day(5, 3, 10, "Ch10: contrastive (SimCLR/MoCo/BYOL) narrative", 3)
add_day(5, 4, 10, "Ch10: MAE + DINO/v2/v3 + frozen-backbone story", 3)
add_day(5, 5, 10, "Ch10: DINOv3 frozen-backbone seg notebook", 3)

# Week 6: Ch 11 (Mon-Tue), Ch 12 (Wed-Thu), Ch 13 (Fri-Sat)
add_day(6, 0, 11, "Ch11: CLIP/SigLIP/EVA-CLIP + retrieval theory", 3)
add_day(6, 1, 11, "Ch11: photo search app (CLIP + FAISS) + prompt engineering", 3)
add_day(6, 2, 12, "Ch12: GAN/VAE narrative + diffusion DDPM math", 4)
add_day(6, 3, 12, "Ch12: SD 3.5/Flux/SDXL/ControlNet + LoRA fine-tune notebook", 4)
add_day(6, 4, 13, "Ch13: VLM anatomy + LLaVA/Qwen-VL/Florence-3 + Claude/GPT-4o/Gemini", 3)
add_day(6, 5, 13, "Ch13: Claude Vision doc Q&A + Qwen2.5-VL fallback notebook", 3)

# Week 7: Ch 14 (Mon-Tue), Ch 15 (Wed-Thu), Ch 16 (Fri-Sat)
add_day(7, 0, 14, "Ch14: OCR/layout (PaddleOCR/Donut/LayoutLM) + structured-output VLMs", 3)
add_day(7, 1, 14, "Ch14: visual agent loop + invoice + browser-agent notebook", 3)
add_day(7, 2, 15, "Ch15: optical flow + 3D CNNs + VideoMAE narrative", 3)
add_day(7, 3, 15, "Ch15: tracking (SORT→ByteTrack→SAM 2) + sports-analytics demo", 3)
add_day(7, 4, 16, "Ch16: depth + point clouds + COLMAP + NeRF lineage", 4)
add_day(7, 5, 16, "Ch16: 3DGS + Nerfstudio + phone-capture fly-through notebook", 4)

# Week 8: Ch 17 (Mon-Tue), Ch 18 (Wed), Ch 19 (Thu), Ch 20 (Fri), Pass (Sat)
add_day(8, 0, 17, "Ch17: VLA paradigm + RT-2/OpenVLA/π0/Helix narrative", 4)
add_day(8, 1, 17, "Ch17: OpenVLA simulation + attention viz notebook", 4)
add_day(8, 2, 18, "Ch18: Medical (MONAI) + AV (BEV) + Geospatial + Agriculture", 4)
add_day(8, 3, 19, "Ch19: quantization + ONNX/TensorRT/CoreML + Jetson benchmark", 4)
add_day(8, 4, 20, "Ch20: MLOps + responsible AI + future + capstone integration", 4)
add_day(8, 5, None, "Cross-chapter pass: forward refs, dedup, transitions, figure polish", 5)


def style_header(cell, fill=BLUE, font_color=WHITE, bold=True):
    cell.fill = PatternFill('solid', fgColor=fill)
    cell.font = Font(name='Calibri', size=11, bold=bold, color=font_color)
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    cell.border = Border(
        left=Side('thin', color='CCCCCC'), right=Side('thin', color='CCCCCC'),
        top=Side('thin', color='CCCCCC'), bottom=Side('thin', color='CCCCCC'),
    )


def style_cell(cell, fill=None, bold=False, wrap=True, color='222222', size=10):
    if fill:
        cell.fill = PatternFill('solid', fgColor=fill)
    cell.font = Font(name='Calibri', size=size, bold=bold, color=color)
    cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=wrap)
    cell.border = Border(
        left=Side('thin', color='DDDDDD'), right=Side('thin', color='DDDDDD'),
        top=Side('thin', color='DDDDDD'), bottom=Side('thin', color='DDDDDD'),
    )


def main():
    wb = Workbook()

    # ========== Sheet 1: Overview ==========
    ws = wb.active
    ws.title = 'Overview'

    ws['A1'] = 'Computer Vision: From Foundations to Frontier'
    ws['A1'].font = Font(name='Calibri', size=20, bold=True, color=BLUE)
    ws.merge_cells('A1:F1')

    ws['A2'] = '20-Chapter Book — 8-Week Writing Plan'
    ws['A2'].font = Font(name='Calibri', size=13, italic=True, color=GRAY)
    ws.merge_cells('A2:F2')

    ws['A4'] = 'Author'
    ws['B4'] = 'Milan Amrut Joshi'
    ws['A5'] = 'Start date'
    ws['B5'] = START_DATE.strftime('%Y-%m-%d (Mon)')
    ws['A6'] = 'Target words/chapter'
    ws['B6'] = '~3,000'
    ws['A7'] = 'Total target words'
    ws['B7'] = sum(c[2] for c in CHAPTERS)
    ws['A8'] = 'Working days'
    ws['B8'] = 6
    ws['A9'] = 'Hours/day'
    ws['B9'] = '3 (writing + code)'
    ws['A10'] = 'Buffer week'
    ws['B10'] = 'Week 9 (revision sprint)'

    for row in range(4, 11):
        ws[f'A{row}'].font = Font(name='Calibri', size=11, bold=True, color=BLUE)
        ws[f'B{row}'].font = Font(name='Calibri', size=11)

    ws['A12'] = 'Weekly Summary'
    ws['A12'].font = Font(name='Calibri', size=14, bold=True, color=BLUE)
    ws.merge_cells('A12:F12')

    headers = ['Week', 'Dates', 'Chapters', 'Target Words', 'Difficulty', 'Notes']
    for i, h in enumerate(headers):
        cell = ws.cell(row=13, column=i+1, value=h)
        style_header(cell)

    week_notes = {
        0: 'Pre-launch: repo, dataset, template',
        1: 'Foundations warm-up — fast wins',
        2: 'Geometry-heavy week — figures matter',
        3: 'CNN core + training tricks',
        4: 'Detection + segmentation. Mid-book consistency pass',
        5: 'ViTs + self-supervised (DINOv3)',
        6: 'Hardest chapter (Diffusion) lands here',
        7: 'Multimodal frontier + 3D Gaussian Splatting',
        8: 'VLA + Domains + Edge + MLOps + cross-pass',
    }

    row = 14
    for week_num in range(0, 9):
        chapters_in_week = WEEK_PLAN.get(week_num, [])
        ch_str = '—' if not chapters_in_week else ', '.join(f'Ch{c}' for c in chapters_in_week)
        words = sum(c[2] for c in CHAPTERS if c[0] in chapters_in_week)
        diffs = [c[3] for c in CHAPTERS if c[0] in chapters_in_week]
        diff_str = '—' if not diffs else f'{sum(diffs)/len(diffs):.1f}/5'
        week_start = START_DATE + timedelta(weeks=week_num)
        week_end = week_start + timedelta(days=5)
        date_str = f'{week_start.strftime("%b %d")} – {week_end.strftime("%b %d")}'

        ws.cell(row=row, column=1, value=f'Week {week_num}')
        ws.cell(row=row, column=2, value=date_str)
        ws.cell(row=row, column=3, value=ch_str)
        ws.cell(row=row, column=4, value=words if words else '—')
        ws.cell(row=row, column=5, value=diff_str)
        ws.cell(row=row, column=6, value=week_notes[week_num])

        fill = LIGHT_BLUE if week_num % 2 == 0 else WHITE
        for col in range(1, 7):
            style_cell(ws.cell(row=row, column=col), fill=fill, wrap=True)
        ws.cell(row=row, column=1).font = Font(name='Calibri', size=11, bold=True, color=BLUE)
        row += 1

    # Column widths
    widths = [10, 22, 22, 14, 12, 50]
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i+1)].width = w

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 20

    # ========== Sheet 2: Chapter Plan ==========
    ws2 = wb.create_sheet('Chapter Plan')
    ws2['A1'] = 'Chapter Plan — All 20 Chapters'
    ws2['A1'].font = Font(name='Calibri', size=18, bold=True, color=BLUE)
    ws2.merge_cells('A1:H1')

    headers2 = ['#', 'Chapter Title', 'Week', 'Target Words', 'Difficulty (1-5)',
                'Hands-On Project', 'Status', 'Actual Words']
    for i, h in enumerate(headers2):
        cell = ws2.cell(row=3, column=i+1, value=h)
        style_header(cell)

    for i, (num, title, words, diff, hands_on) in enumerate(CHAPTERS):
        r = i + 4
        # Find which week
        week_assigned = next((wk for wk, chs in WEEK_PLAN.items() if num in chs), None)
        ws2.cell(row=r, column=1, value=num)
        ws2.cell(row=r, column=2, value=title)
        ws2.cell(row=r, column=3, value=f'Week {week_assigned}' if week_assigned else '')
        ws2.cell(row=r, column=4, value=words)
        ws2.cell(row=r, column=5, value=diff)
        ws2.cell(row=r, column=6, value=hands_on)
        ws2.cell(row=r, column=7, value='Not started')
        ws2.cell(row=r, column=8, value=0)

        fill = LIGHT_BLUE if i % 2 == 0 else WHITE
        for col in range(1, 9):
            cell = ws2.cell(row=r, column=col)
            style_cell(cell, fill=fill)
            if col in (1, 4, 5, 8):
                cell.alignment = Alignment(horizontal='center', vertical='top')

    # Status validation list
    from openpyxl.worksheet.datavalidation import DataValidation
    dv = DataValidation(type='list', formula1='"Not started,Outlining,Drafting,Code,Edit,Done"', allow_blank=True)
    ws2.add_data_validation(dv)
    dv.add(f'G4:G{3+len(CHAPTERS)}')

    # Conditional formatting for difficulty
    from openpyxl.styles import PatternFill as PF
    diff_fills = {
        1: PF('solid', fgColor='C8EBC8'),
        2: PF('solid', fgColor='E0F2C0'),
        3: PF('solid', fgColor='FFEFB0'),
        4: PF('solid', fgColor='FFD499'),
        5: PF('solid', fgColor='F4B7B7'),
    }
    for i, (num, _, _, diff, _) in enumerate(CHAPTERS):
        cell = ws2.cell(row=i+4, column=5)
        cell.fill = diff_fills[diff]

    # Done row highlight via conditional formatting
    green_fill = PF('solid', fgColor=LIGHT_GREEN)
    rule = FormulaRule(formula=[f'$G4="Done"'], fill=green_fill)
    ws2.conditional_formatting.add(f'A4:H{3+len(CHAPTERS)}', rule)

    widths2 = [5, 50, 10, 14, 14, 50, 14, 14]
    for i, w in enumerate(widths2):
        ws2.column_dimensions[get_column_letter(i+1)].width = w

    ws2.row_dimensions[1].height = 26
    for r in range(4, 4+len(CHAPTERS)):
        ws2.row_dimensions[r].height = 32

    # Totals row
    total_row = 4 + len(CHAPTERS) + 1
    ws2.cell(row=total_row, column=2, value='TOTAL').font = Font(bold=True, color=BLUE, size=12)
    ws2.cell(row=total_row, column=4, value=f'=SUM(D4:D{3+len(CHAPTERS)})').font = Font(bold=True, color=BLUE)
    ws2.cell(row=total_row, column=8, value=f'=SUM(H4:H{3+len(CHAPTERS)})').font = Font(bold=True, color=BLUE)
    progress_row = total_row + 1
    ws2.cell(row=progress_row, column=2, value='PROGRESS').font = Font(bold=True, color=GREEN, size=12)
    ws2.cell(row=progress_row, column=4, value=f'=IFERROR(H{total_row}/D{total_row},0)').number_format = '0.0%'
    ws2.cell(row=progress_row, column=4).font = Font(bold=True, color=GREEN)

    ws2.freeze_panes = 'A4'

    # ========== Sheet 3: Daily Schedule ==========
    ws3 = wb.create_sheet('Daily Schedule')
    ws3['A1'] = 'Daily Writing Schedule (Mon–Sat, 6 days/week)'
    ws3['A1'].font = Font(name='Calibri', size=18, bold=True, color=BLUE)
    ws3.merge_cells('A1:G1')

    headers3 = ['Day #', 'Date', 'Week', 'Day', 'Chapter', 'Activity', 'Hours', 'Done?']
    for i, h in enumerate(headers3):
        cell = ws3.cell(row=3, column=i+1, value=h)
        style_header(cell)

    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    for i, (week, dow, ch, activity, hours) in enumerate(DAILY_PLAN):
        r = i + 4
        d = START_DATE + timedelta(weeks=week, days=dow)
        ws3.cell(row=r, column=1, value=i+1)
        ws3.cell(row=r, column=2, value=d.strftime('%Y-%m-%d'))
        ws3.cell(row=r, column=3, value=f'Week {week}')
        ws3.cell(row=r, column=4, value=day_names[dow])
        ws3.cell(row=r, column=5, value=f'Ch{ch}' if ch else '—')
        ws3.cell(row=r, column=6, value=activity)
        ws3.cell(row=r, column=7, value=hours)
        ws3.cell(row=r, column=8, value='')

        fill = LIGHT_GRAY if week % 2 == 0 else WHITE
        if week == 0:
            fill = LIGHT_ORANGE
        for col in range(1, 9):
            cell = ws3.cell(row=r, column=col)
            style_cell(cell, fill=fill)
            if col in (1, 7, 8):
                cell.alignment = Alignment(horizontal='center', vertical='top')

    # Hard chapters highlight (diff 4-5)
    hard_fill = PF('solid', fgColor='FCE4E4')
    for i, (week, dow, ch, _, _) in enumerate(DAILY_PLAN):
        if ch:
            ch_diff = next((c[3] for c in CHAPTERS if c[0] == ch), 0)
            if ch_diff >= 4:
                ws3.cell(row=i+4, column=5).fill = hard_fill

    # Done validation
    dv2 = DataValidation(type='list', formula1='"☐,☑"', allow_blank=True)
    ws3.add_data_validation(dv2)
    dv2.add(f'H4:H{3+len(DAILY_PLAN)}')

    widths3 = [7, 12, 9, 6, 8, 70, 8, 9]
    for i, w in enumerate(widths3):
        ws3.column_dimensions[get_column_letter(i+1)].width = w

    ws3.row_dimensions[1].height = 26
    for r in range(4, 4+len(DAILY_PLAN)):
        ws3.row_dimensions[r].height = 26

    ws3.freeze_panes = 'A4'

    # ========== Sheet 4: Daily Routine ==========
    ws4 = wb.create_sheet('Daily Routine')
    ws4['A1'] = 'Daily Routine That Makes 8 Weeks Possible'
    ws4['A1'].font = Font(name='Calibri', size=18, bold=True, color=BLUE)
    ws4.merge_cells('A1:C1')

    routine = [
        ('Time', 'Activity', 'Why'),
        ('Morning (90 min)', 'Drafting prose for current chapter', 'No research, no rabbit holes — pure output. Highest energy hours.'),
        ('Midday (60 min)', 'Code / notebook for current chapter', 'Code first, prose around it. Notebook drives the explanation.'),
        ('Evening (30 min)', 'Outline tomorrow + collect 2-3 references', 'Avoid blank-page friction at start of next session.'),
        ('', '', ''),
        ('Weekly', 'Saturday is buffer / catch-up', 'Sunday off. Avoid burnout.'),
        ('Mid-book (end Week 4)', 'Half-day consistency pass on Ch 1-8', 'Catch voice drift early; build cross-references list.'),
        ('Weekly check', 'Update Chapter Plan status + actual words', 'Tracks momentum honestly.'),
    ]

    for i, row_data in enumerate(routine):
        r = i + 3
        for j, val in enumerate(row_data):
            cell = ws4.cell(row=r, column=j+1, value=val)
            if i == 0:
                style_header(cell)
            else:
                fill = LIGHT_BLUE if i % 2 == 1 else WHITE
                style_cell(cell, fill=fill, bold=(j == 0))

    ws4.column_dimensions['A'].width = 24
    ws4.column_dimensions['B'].width = 40
    ws4.column_dimensions['C'].width = 65
    for r in range(4, 4+len(routine)-1):
        ws4.row_dimensions[r].height = 32

    # ========== Sheet 5: Risks ==========
    ws5 = wb.create_sheet('Risks & Mitigations')
    ws5['A1'] = 'Risks and Mitigations'
    ws5['A1'].font = Font(name='Calibri', size=18, bold=True, color=BLUE)
    ws5.merge_cells('A1:C1')

    risks = [
        ('Risk', 'Mitigation', 'Trigger'),
        ('Hardest chapters (Diffusion Ch12, VLA Ch17, 3DGS Ch16) bog down whole plan',
         'Schedule them in peak weeks (5-7), not the last week. Pre-research one week ahead.',
         'When draft progress for these chapters falls behind by >1 day'),
        ('Code breaks across library upgrades',
         'Pin every dependency in a per-chapter requirements.txt; snapshot Colab-compatible env',
         'Any "it worked yesterday" moment'),
        ('"Just one more reference" rabbit hole',
         'Hard-cap research at 30 min/day per chapter; missing items become footnotes for revision pass',
         'When research time exceeds writing time on any day'),
        ('Energy dip in Week 5 (statistically common)',
         'Pre-book a no-meetings, single-coffee-shop writing day to break the slump',
         'Two consecutive low-output days'),
        ('Voice / tone drift across chapters',
         'Mid-book consistency pass at end of Week 4 (built into schedule)',
         'When re-reading earlier chapters feels like another author wrote them'),
        ('VLA / SAM 3 / SD 3.5 lib changes mid-writing',
         'Lock model versions; note "as of Apr 2026" inline so updates are easy',
         'Major release announcement during writing period'),
        ('Underestimating revision time',
         'Reserve full Week 9 buffer for revision + reviewer feedback',
         'When draft completes but reviewers find structural issues'),
    ]

    for i, row_data in enumerate(risks):
        r = i + 3
        for j, val in enumerate(row_data):
            cell = ws5.cell(row=r, column=j+1, value=val)
            if i == 0:
                style_header(cell)
            else:
                fill = LIGHT_ORANGE if i % 2 == 1 else WHITE
                style_cell(cell, fill=fill, bold=(j == 0))

    ws5.column_dimensions['A'].width = 50
    ws5.column_dimensions['B'].width = 60
    ws5.column_dimensions['C'].width = 45
    for r in range(4, 4+len(risks)-1):
        ws5.row_dimensions[r].height = 50

    # ========== Sheet 6: Word Count Tracker ==========
    ws6 = wb.create_sheet('Word Tracker')
    ws6['A1'] = 'Daily Word Count Tracker'
    ws6['A1'].font = Font(name='Calibri', size=18, bold=True, color=BLUE)
    ws6.merge_cells('A1:E1')

    tr_headers = ['Date', 'Day', 'Words Drafted', 'Cumulative', 'Notes']
    for i, h in enumerate(tr_headers):
        cell = ws6.cell(row=3, column=i+1, value=h)
        style_header(cell)

    # Pre-fill 9 weeks of dates (Mon-Sat)
    row_idx = 4
    for w in range(9):
        for d in range(6):
            day_date = START_DATE + timedelta(weeks=w, days=d)
            ws6.cell(row=row_idx, column=1, value=day_date.strftime('%Y-%m-%d'))
            ws6.cell(row=row_idx, column=2, value=day_names[d])
            if row_idx == 4:
                ws6.cell(row=row_idx, column=4, value=f'=C{row_idx}')
            else:
                ws6.cell(row=row_idx, column=4, value=f'=D{row_idx-1}+C{row_idx}')
            fill = LIGHT_BLUE if w % 2 == 0 else WHITE
            for col in range(1, 6):
                cell = ws6.cell(row=row_idx, column=col)
                style_cell(cell, fill=fill)
                if col in (3, 4):
                    cell.alignment = Alignment(horizontal='right', vertical='top')
            row_idx += 1

    ws6.column_dimensions['A'].width = 14
    ws6.column_dimensions['B'].width = 8
    ws6.column_dimensions['C'].width = 16
    ws6.column_dimensions['D'].width = 16
    ws6.column_dimensions['E'].width = 50

    # Goal cell
    ws6['F3'] = 'Goal'
    ws6['F3'].font = Font(bold=True, color=BLUE, size=11)
    ws6['G3'] = sum(c[2] for c in CHAPTERS)
    ws6['G3'].font = Font(bold=True)
    ws6['F4'] = 'Cumulative %'
    ws6['F4'].font = Font(bold=True, color=GREEN, size=11)
    ws6['G4'] = f'=IFERROR(D{row_idx-1}/G3, 0)'
    ws6['G4'].number_format = '0.0%'
    ws6['G4'].font = Font(bold=True, color=GREEN)

    ws6.freeze_panes = 'A4'

    # Save
    out = 'WRITING_PLAN.xlsx'
    wb.save(out)
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
