"""
Simple PDF generation from markdown
"""
import markdown
from pathlib import Path

# Read markdown
md_content = Path('APPROACH_DOCUMENT.md').read_text(encoding='utf-8')

# Convert to HTML
html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'nl2br'])

# Create styled HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SHL Assessment System - Technical Approach</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 10pt;
            max-width: 100%;
        }}
        h1 {{
            color: #00b894;
            border-bottom: 3px solid #00d4aa;
            padding-bottom: 8px;
            font-size: 20pt;
            margin-top: 0;
        }}
        h2 {{
            color: #00d4aa;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 14pt;
            page-break-after: avoid;
        }}
        h3 {{
            color: #555;
            font-size: 11pt;
            margin-top: 15px;
            page-break-after: avoid;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
            font-size: 9pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 6px;
            text-align: left;
        }}
        th {{
            background-color: #00d4aa;
            color: white;
            font-weight: bold;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
            font-size: 9pt;
        }}
        pre {{
            background: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 8pt;
        }}
        strong {{
            color: #00b894;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        p {{
            margin: 8px 0;
        }}
        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

# Save HTML
output_file = 'SHL_Assessment_System_Approach.html'
Path(output_file).write_text(html_content, encoding='utf-8')

print(f"✓ Generated {output_file}")
print("\nTo convert to PDF:")
print("1. Open the HTML file in your browser")
print("2. Press Ctrl+P (Print)")
print("3. Select 'Save as PDF'")
print("4. Save as: SHL_Assessment_System_Approach.pdf")
