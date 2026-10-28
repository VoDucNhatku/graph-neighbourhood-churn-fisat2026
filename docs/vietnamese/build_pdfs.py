"""Render the Vietnamese study documents with embedded fonts and readable maths.

Run: python docs/vietnamese/build_pdfs.py [--only 01|02|03|04]
Dependencies: reportlab, matplotlib, pillow, pymupdf.
"""
from pathlib import Path
from xml.sax.saxutils import escape
from urllib.parse import quote
import argparse
import hashlib
import json
import re
import unicodedata

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Image, LongTable, TableStyle, KeepTogether, HRFlowable, Flowable)
from reportlab.platypus.tableofcontents import TableOfContents
import matplotlib
matplotlib.use("Agg")
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties

ROOT = Path(__file__).resolve().parents[2]
SOURCES = Path(__file__).resolve().parent
OUTPUT = ROOT / "output/pdf"
TEMP = ROOT / "tmp/pdfs"
MATH = TEMP / "math"
REPO_URL = "https://github.com/VoDucNhatku/graph-neighbourhood-churn-fisat2026"
PAGE_W, PAGE_H = A4
MARGIN_X = 46
CONTENT_W = PAGE_W - 2*MARGIN_X
INK = colors.HexColor("#203044")
ACCENT = colors.HexColor("#14736A")
LIGHT = colors.HexColor("#EDF5F3")
GRAY = colors.HexColor("#617083")
RULE = colors.HexColor("#D9E2E8")
SPECS = [
    ("01", "01-kien-thuc-nen-tang.md", "01-kien-thuc-nen-tang-paper.pdf", "Sổ tay kiến thức", "Hiểu paper từ nền tảng đến kiểm định và tái lập"),
    ("02", "02-quy-trinh-nghien-cuu.md", "02-quy-trinh-nghien-cuu.pdf", "Quy trình nghiên cứu", "Từ câu hỏi nghiên cứu đến bằng chứng và báo cáo kết quả"),
    ("03", "03-ban-dich-paper.md", "03-ban-dich-paper-tieng-viet.pdf", "Bản dịch toàn bộ paper", "Bản dịch trung thành của phiên bản đã được chấp nhận"),
    ("04", "04-bao-cao-tong-hop.md", "04-bao-cao-tong-hop.pdf", "Báo cáo tổng hợp", "Hồ sơ hội nghị, thực nghiệm và các điểm cần xử lý"),
]


def font_setup():
    candidates = [
        (Path("C:/Windows/Fonts"), ["arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"]),
        (Path("/usr/share/fonts/truetype/dejavu"), ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans-Oblique.ttf", "DejaVuSans-BoldOblique.ttf"]),
    ]
    for folder, filenames in candidates:
        if all((folder/name).exists() for name in filenames):
            for suffix, filename in zip(["", "-Bold", "-Italic", "-BoldItalic"], filenames):
                pdfmetrics.registerFont(TTFont("DocSans"+suffix, str(folder/filename)))
            pdfmetrics.registerFontFamily("DocSans", normal="DocSans", bold="DocSans-Bold",
                                         italic="DocSans-Italic", boldItalic="DocSans-BoldItalic")
            mono = Path("C:/Windows/Fonts/consola.ttf") if folder.drive else folder/"DejaVuSansMono.ttf"
            pdfmetrics.registerFont(TTFont("DocMono", str(mono if mono.exists() else folder/filenames[0])))
            return
    raise RuntimeError("No font with Vietnamese support found. Install Arial or DejaVu Sans.")


def normalized(text):
    return unicodedata.normalize("NFC", text).translate(str.maketrans({
        "\u2011": "-", "\u2013": "-", "\u2014": "-", "\u00a0": " ", "\u200b": ""}))


def math_png(expression, size=11, foreground="#203044"):
    expression = expression.strip().replace("\\text{", "\\mathrm{")
    key = hashlib.sha256((expression+str(size)+foreground+"transparent-v1").encode()).hexdigest()[:24]
    path = MATH/(key+".png")
    if not path.exists():
        math_to_image("$"+expression+"$", path, prop=FontProperties(size=size), dpi=220,
                      format="png", color="#203044")
        # Convert the white mathtext canvas to true transparency, then tint the
        # glyphs for dark table headers without changing the mathematical content.
        with PILImage.open(path) as rendered:
            rendered=rendered.convert("RGBA")
            rgb=tuple(int(foreground[i:i+2],16) for i in [1,3,5])
            values=rendered.get_flattened_data() if hasattr(rendered,"get_flattened_data") else rendered.getdata()
            pixels=[(*rgb,max(0,min(255,round((255-r)*255/223)))) for r,g,b,a in values]
            rendered.putdata(pixels)
            rendered.save(path)
    with PILImage.open(path) as source:
        width, height = source.size
    return path, width*72/220, height*72/220


def link_target(url):
    if re.match(r"https?://|mailto:|#", url):
        return url
    resolved = (SOURCES/url.split("#", 1)[0]).resolve()
    try:
        relative = resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return REPO_URL
    suffix = "#"+url.split("#", 1)[1] if "#" in url else ""
    return REPO_URL+"/blob/main/"+quote(relative, safe="/")+suffix


def inline(text, cell=False, header=False):
    text = normalized(text)
    items = []
    def keep(html):
        token = f"ZXQTOKEN{len(items)}QXZ"
        items.append(html)
        return token
    text = re.sub(r"`([^`]+)`", lambda m: keep('<font size="9" color="#14736A">'+escape(m[1])+"</font>"), text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: keep('<link href="'+escape(link_target(m[2]))+'" color="#14736A">'+escape(m[1])+"</link>"), text)
    def formula(match):
        path, width, height = math_png(match[1], 9.5 if cell else 10.3,
                                      "#ffffff" if header else "#203044")
        scale = min(1, 17/max(height, 1), (CONTENT_W*.9)/max(width, 1))
        return keep(f'<img src="{escape(str(path))}" width="{width*scale:.3f}" height="{height*scale:.3f}" valign="-3"/>')
    text = re.sub(r"\$([^$\n]+)\$", formula, text)
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for index, item in enumerate(items):
        text = text.replace(f"ZXQTOKEN{index}QXZ", item)
    if cell:
        text=text.replace("Graph-Enhanced","Graph-<br/>Enhanced")
    return text


def styles():
    common = {"fontName": "DocSans", "textColor": INK, "splitLongWords": True,
              "allowWidows": 0, "allowOrphans": 0}
    return {
        "body": ParagraphStyle("Body", fontSize=10.3, leading=15.4, spaceAfter=7, **common),
        "h1": ParagraphStyle("H1", fontSize=16.5, leading=22, fontName="DocSans-Bold",
                              textColor=ACCENT, spaceBefore=17, spaceAfter=10, keepWithNext=True),
        "h2": ParagraphStyle("H2", fontSize=12.7, leading=18, fontName="DocSans-Bold",
                              textColor=INK, spaceBefore=12, spaceAfter=7, keepWithNext=True),
        "h3": ParagraphStyle("H3", fontSize=11.1, leading=16, fontName="DocSans-Bold",
                              textColor=INK, spaceBefore=9, spaceAfter=5, keepWithNext=True),
        "cell": ParagraphStyle("Cell", fontSize=9.0, leading=12.5, spaceAfter=0, **common),
        "cellhead": ParagraphStyle("CellHead", fontSize=9.0, leading=12.5, fontName="DocSans-Bold", textColor=colors.white),
        "caption": ParagraphStyle("Caption", fontSize=9.2, leading=13.5, alignment=TA_LEFT, spaceBefore=5, spaceAfter=10, **common),
        "quote": ParagraphStyle("Quote", fontSize=10.0, leading=15, leftIndent=10, rightIndent=10,
                                borderColor=RULE, borderPadding=8, backColor=LIGHT, spaceAfter=9, **common),
        "bullet": ParagraphStyle("Bullet", fontSize=10.3, leading=15.4, leftIndent=13, firstLineIndent=-10,
                                 spaceAfter=5, **common),
        "code": ParagraphStyle("Code", fontSize=8.8, leading=13.0, fontName="DocMono", textColor=INK),
    }


class CodeBlock(Flowable):
    """Draw one background before all code lines; split only at line boundaries.

    Per-line Paragraph backgrounds with borderPadding painted over preceding
    glyphs. Measuring actual font widths also avoids an arbitrary character cap.
    """
    padding = 10

    def __init__(self, lines, style):
        super().__init__()
        self.lines = lines
        self.style = style
        self.spaceBefore = 5
        self.spaceAfter = 10

    def wrap(self, available_width, available_height):
        self.width = available_width
        text_width = available_width - 2*self.padding
        wrapped = []
        for line in self.lines:
            remaining = normalized(line.expandtabs(4))
            if not remaining:
                wrapped.append("")
            while remaining:
                cut = len(remaining)
                while cut > 1 and pdfmetrics.stringWidth(remaining[:cut], self.style.fontName,
                                                        self.style.fontSize) > text_width:
                    cut -= 1
                wrapped.append(remaining[:cut])
                remaining = remaining[cut:]
        self.wrapped = wrapped
        self.height = 2*self.padding + len(wrapped)*self.style.leading
        return self.width, self.height

    def split(self, available_width, available_height):
        if len(self.wrapped) <= 12:
            return []
        count = int((available_height-2*self.padding)//self.style.leading)
        if count < 2:
            return []
        return [CodeBlock(self.wrapped[:count], self.style),
                CodeBlock(self.wrapped[count:], self.style)]

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#F4F6F8"))
        canvas.setStrokeColor(RULE)
        canvas.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        canvas.setFillColor(INK)
        canvas.setFont(self.style.fontName, self.style.fontSize)
        y = self.height-self.padding-self.style.fontSize
        for line in self.wrapped:
            canvas.drawString(self.padding, y, line)
            y -= self.style.leading
        canvas.restoreState()


class StudyDoc(BaseDocTemplate):
    def __init__(self, path, label, **kwargs):
        self.label = label
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN_X, rightMargin=MARGIN_X,
                         topMargin=52, bottomMargin=48, title=label,
                         author="Duc Nhat Vo - Tai lieu tieng Viet", **kwargs)
        frame = Frame(MARGIN_X, 48, CONTENT_W, PAGE_H-100, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0, id="normal")
        self.addPageTemplates(PageTemplate(id="study", frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(RULE)
            canvas.line(MARGIN_X, PAGE_H-34, PAGE_W-MARGIN_X, PAGE_H-34)
            canvas.setFont("DocSans", 8.2)
            canvas.setFillColor(GRAY)
            canvas.drawString(MARGIN_X, PAGE_H-27, self.label)
            canvas.drawRightString(PAGE_W-MARGIN_X, PAGE_H-27, "Paper #366956")
        canvas.setStrokeColor(RULE)
        canvas.line(MARGIN_X, 34, PAGE_W-MARGIN_X, 34)
        canvas.setFont("DocSans", 8)
        canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN_X, 21, "Tài liệu học tập và đối chiếu | 13/10/2026")
        canvas.drawRightString(PAGE_W-MARGIN_X, 21, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and hasattr(flowable, "heading_level"):
            key = flowable.bookmark_key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=flowable.heading_level, closed=False)
            self.notify("TOCEntry", (flowable.heading_level, flowable.getPlainText(), self.page, key))


def table(lines, st):
    rows = [[c.strip().replace("\\|", "|") for c in line.strip().strip("|").split("|")] for line in lines]
    rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c) for c in r)]
    count = max(len(r) for r in rows)
    for row in rows:
        row.extend([""]*(count-len(row)))
    # Allocate more width to prose columns and cap domination by one long cell.
    weights = [min(65, max(13, max(len(re.sub(r"[$*`]", "", r[i])) for r in rows)))**.7 for i in range(count)]
    widths = [CONTENT_W*w/sum(weights) for w in weights]
    data = [[Paragraph(inline(value, cell=True, header=ri==0), st["cellhead" if ri == 0 else "cell"])
             for value in row] for ri, row in enumerate(rows)]
    output = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1, splitInRow=1)
    output.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ACCENT),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F4F8F7")]),
        ("LINEBELOW", (0,0), (-1,0), .5, ACCENT),
        ("LINEBELOW", (0,1), (-1,-1), .3, RULE),
    ]))
    return output


def parse_markdown(source, st):
    lines = source.splitlines()
    flow = []
    index = 0
    headings = []
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("```"):
            if line[3:].strip().lower() == "mermaid":
                raise ValueError("Render Mermaid as a labelled figure before creating a PDF; raw diagram code is forbidden.")
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            flow.append(CodeBlock(code_lines, st["code"]))
            index += 1
            continue
        if line.startswith("$$"):
            expression = line[2:]
            if expression.endswith("$$"):
                expression = expression[:-2]
            else:
                index += 1
                chunks = [expression]
                while index < len(lines) and "$$" not in lines[index]:
                    chunks.append(lines[index])
                    index += 1
                if index < len(lines):
                    chunks.append(lines[index].split("$$")[0])
                expression = " ".join(chunks)
            path, width, height = math_png(expression, 12)
            scale = min(1, CONTENT_W/max(width, 1))
            image = Image(str(path), width=width*scale, height=height*scale)
            image.hAlign = "CENTER"
            flow.extend([Spacer(1, 6), image, Spacer(1, 10)])
            index += 1
            continue
        if line.startswith("|") and index+1 < len(lines) and re.match(r"\s*\|?\s*:?-{2,}", lines[index+1]):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            rendered_table = table(table_lines, st)
            table_height = rendered_table.wrap(CONTENT_W, PAGE_H-100)[1]
            flow.extend([KeepTogether([rendered_table]) if table_height <= 250 else rendered_table,
                         Spacer(1, 11)])
            continue
        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image_match:
            caption, filename = image_match.groups()
            path = (SOURCES/filename).resolve()
            if not path.exists():
                raise FileNotFoundError(f"Missing document image: {path}")
            with PILImage.open(path) as image_source:
                width, height = image_source.size
            scale = min(CONTENT_W/width, 365/height)
            image = Image(str(path), width=width*scale, height=height*scale)
            flow.append(KeepTogether([Spacer(1, 6), image, Paragraph(inline(caption), st["caption"])]))
            index += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            depth, content = len(heading[1]), heading[2]
            if depth == 1 and not headings:
                index += 1
                headings.append((0, content))
                continue
            level = max(0, min(depth-2, 2))
            if depth == 1:
                level = 0
            paragraph = Paragraph(inline(content), st[["h1", "h2", "h3"][level]])
            if level < 2:
                paragraph.heading_level = level
                paragraph.bookmark_key = f"heading-{len(headings)}"
            headings.append((depth, content))
            flow.append(paragraph)
            index += 1
            continue
        if re.fullmatch(r"[-*_]{3,}", line):
            flow.append(HRFlowable(width="100%", thickness=.5, color=RULE, spaceBefore=7, spaceAfter=9))
            index += 1
            continue
        if line.startswith(">"):
            chunks = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                chunks.append(lines[index].strip()[1:].strip())
                index += 1
            flow.append(Paragraph(inline(" ".join(chunks)), st["quote"]))
            continue
        item = re.match(r"^(?:([-*])\s+|(\d+[.)])\s+)(.+)$", line)
        if item:
            prefix = "•" if item[1] else item[2]
            flow.append(Paragraph(inline(prefix+" "+item[3]), st["bullet"]))
            index += 1
            continue
        chunks = [line]
        index += 1
        while index < len(lines) and lines[index].strip() and not re.match(r"^(#{1,6}\s|\||\$\$|```|>|!\[|[-*]\s|\d+[.)]\s)", lines[index].strip()):
            chunks.append(lines[index].strip())
            index += 1
        flow.append(Paragraph(inline(" ".join(chunks)), st["body"]))
    return flow, headings


def build(spec):
    number, filename, pdfname, label, subtitle = spec
    source_path = SOURCES/filename
    source = source_path.read_text(encoding="utf-8")
    st = styles()
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("TOC0", fontName="DocSans-Bold", fontSize=10.0, leading=14.5,
                       spaceBefore=6, textColor=INK, rightIndent=22),
        ParagraphStyle("TOC1", fontName="DocSans", fontSize=9.2, leading=13,
                       leftIndent=14, textColor=GRAY, rightIndent=22),
    ]
    title_style = ParagraphStyle("CoverTitle", fontName="DocSans-Bold", fontSize=28, leading=36, textColor=INK)
    subtitle_style = ParagraphStyle("CoverSubtitle", fontName="DocSans", fontSize=14, leading=22, textColor=GRAY)
    story = [Spacer(1, 67), Paragraph("TÀI LIỆU TIẾNG VIỆT / "+number, st["h2"]), Spacer(1, 15),
             Paragraph(label, title_style), Spacer(1, 16), Paragraph(subtitle, subtitle_style),
             Spacer(1, 25), HRFlowable(width="28%", thickness=4, color=ACCENT, hAlign="LEFT"), Spacer(1, 27),
             Paragraph("Paper #366956 · EAI FISAT 2026", st["h2"]),
             Paragraph("When Graph-Derived Neighbourhood Features Do Not Help: A Leakage-Controlled Evaluation of Behavioural-LRFM Churn Prediction in Non-Contractual Retail", st["body"]),
             Spacer(1, 14), Paragraph("Dành cho nhóm đã biết Python và machine learning cơ bản.<br/>Phiên bản tài liệu: 13/10/2026. Nguồn: paper, code và bằng chứng tái lập.", st["body"]),
             PageBreak(), Paragraph("Mục lục", st["h1"]), toc, PageBreak()]
    body, headings = parse_markdown(source, st)
    story.extend(body)
    destination = OUTPUT/pdfname
    doc = StudyDoc(destination, label)
    doc.multiBuild(story)
    return {"source": str(source_path.relative_to(ROOT)), "pdf": str(destination.relative_to(ROOT)),
            "bytes": destination.stat().st_size, "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
            "headings": len(headings), "word_count": len(source.split())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", choices=["01", "02", "03", "04"])
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    MATH.mkdir(parents=True, exist_ok=True)
    font_setup()
    result = [build(spec) for spec in SPECS if args.only is None or spec[0] == args.only]
    (TEMP/"build-manifest.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
