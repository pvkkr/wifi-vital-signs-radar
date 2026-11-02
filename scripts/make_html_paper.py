"""
Converts RESEARCH_PAPER_SUBMISSION.md to a publication-formatted, print-ready HTML file.
Students can double-click it and press Ctrl+P to save as a high-quality PDF.
"""

import os
import re

def convert():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path = os.path.join(base_dir, "docs", "RESEARCH_PAPER.md")
    if not os.path.exists(md_path):
        md_path = os.path.join(base_dir, "docs", "RESEARCH_PAPER_SUBMISSION.md")
    html_path = os.path.join(base_dir, "docs", "RESEARCH_PAPER_PRINTABLE.html")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    css = """
    body {
        font-family: 'Times New Roman', Times, serif;
        line-height: 1.5;
        color: #111;
        max-width: 820px;
        margin: 20px auto;
        padding: 30px 45px;
        background: #fff;
    }
    h1 {
        font-size: 22px;
        text-align: center;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .author-block {
        text-align: center;
        font-size: 13px;
        color: #333;
        margin-bottom: 25px;
        border-bottom: 1px solid #ccc;
        padding-bottom: 15px;
    }
    .author-block p {
        margin: 3px 0;
        text-align: center;
    }
    h2 {
        font-size: 15px;
        text-transform: uppercase;
        border-bottom: 1.5px solid #003366;
        padding-bottom: 3px;
        margin-top: 24px;
        color: #003366;
    }
    h3 {
        font-size: 13.5px;
        margin-top: 16px;
        color: #222;
    }
    p, li {
        font-size: 13px;
        text-align: justify;
        margin: 6px 0;
    }
    .abstract-box {
        background: #f7f9fb;
        border-left: 3.5px solid #003366;
        padding: 12px 18px;
        margin: 18px 0;
        font-size: 12.5px;
    }
    .abstract-box h2 {
        border-bottom: none;
        margin-top: 0;
        padding-bottom: 0;
        font-size: 13px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 16px 0;
        font-size: 12px;
    }
    th, td {
        border: 1px solid #888;
        padding: 6px 8px;
        text-align: left;
    }
    th {
        background: #eef2f7;
        font-weight: bold;
    }
    tr:nth-child(even) {
        background: #fafafa;
    }
    pre {
        background: #f4f4f4;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 4px;
        font-family: 'Consolas', monospace;
        font-size: 11px;
        overflow-x: auto;
        line-height: 1.35;
    }
    code {
        font-family: 'Consolas', monospace;
        font-size: 11.5px;
        background: #eee;
        padding: 1px 4px;
        border-radius: 3px;
    }
    pre code {
        background: transparent;
        padding: 0;
    }
    .callout {
        background: #eef6ff;
        border: 1px solid #b8daff;
        padding: 10px 14px;
        border-radius: 4px;
        margin: 12px 0;
        font-size: 12.5px;
    }
    @media print {
        body {
            max-width: 100%;
            margin: 0;
            padding: 12mm 15mm;
        }
        h2 {
            page-break-after: avoid;
        }
        table, pre {
            page-break-inside: avoid;
        }
    }
    """

    # Replace basic markdown elements
    html_body = []
    lines = md_text.split("\n")
    i = 0
    in_code = False
    in_table = False
    in_abstract = False

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            if in_code:
                html_body.append("</code></pre>")
                in_code = False
            else:
                html_body.append("<pre><code>")
                in_code = True
            i += 1
            continue

        if in_code:
            html_body.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
            continue

        # Tables
        if "|" in line:
            if not in_table:
                html_body.append("<table>")
                in_table = True
            if "---" in line:
                i += 1
                continue
            cells = [c.strip() for c in line.split("|")[1:-1]]
            tag = "th" if "Test" in line or "Metric" in line or "Ground" in line else "td"
            row = "<tr>" + "".join([f"<{tag}>{c}</{tag}>" for c in cells]) + "</tr>"
            html_body.append(row)
            i += 1
            continue
        elif in_table:
            html_body.append("</table>")
            in_table = False

        if line.startswith("# "):
            title = line[2:].strip()
            html_body.append(f"<h1>{title}</h1>")
            html_body.append("<div class='author-block'>")
            html_body.append("<p><b>Student Research Submission</b></p>")
            html_body.append("<p>Department of Electronics and Communication Engineering / Computer Science</p>")
            html_body.append("<p>Koneru Lakshmaiah Education Foundation (KL University), Vaddeswaram, A.P.</p>")
            html_body.append("</div>")
        elif line.startswith("## Abstract"):
            html_body.append("<div class='abstract-box'><h2>ABSTRACT</h2>")
            in_abstract = True
        elif in_abstract and line.startswith("## "):
            html_body.append("</div>")
            in_abstract = False
            html_body.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("## "):
            html_body.append(f"<h2>{line[3:].strip()}</h2>")
        elif line.startswith("### "):
            html_body.append(f"<h3>{line[4:].strip()}</h3>")
        elif line.startswith("- "):
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line[2:])
            html_body.append(f"<li>{formatted}</li>")
        elif line.strip() == "":
            pass
        else:
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line)
            html_body.append(f"<p>{formatted}</p>")

        i += 1

    if in_table:
        html_body.append("</table>")
    if in_abstract:
        html_body.append("</div>")

    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Contactless Vital Signs Monitoring Using WiFi CSI - Research Paper</title>
<style>{css}</style>
</head>
<body>
{''.join(html_body)}
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Generated printable HTML paper at: {html_path}")

if __name__ == "__main__":
    convert()
