#!/usr/bin/env python3
"""Convert Markdown files to styled HTML pages matching the doc site theme.

Reads one or more Markdown files and writes corresponding HTML files into an
output directory, reusing the ansible-doc-renderer's CSS when available.

Usage::

    python tools/md_to_html.py \\
        --output docs/_site \\
        --css-path styles.css \\
        docs/12-mcp-server.md docs/13-cli.md

The script uses only the Python standard library — no external markdown
parser is required.  It handles fenced code blocks, tables, headers,
bold/italic, inline code, links, and horizontal rules.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


def _convert_markdown(md: str) -> str:
    """Convert a subset of Markdown to HTML.

    Handles: headings, fenced code blocks, tables, bold, italic,
    inline code, links, horizontal rules, and paragraphs.

    Args:
        md: Raw Markdown string.

    Returns:
        HTML body content string.
    """
    lines = md.split("\n")
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(html.escape(lines[i]))
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            out.append(
                f"<pre><code{cls}>{chr(10).join(code_lines)}</code></pre>"
            )
            continue

        if line.startswith("---") and all(c == "-" for c in line.strip()):
            out.append("<hr>")
            i += 1
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = _inline(heading_match.group(2))
            slug = re.sub(r"[^a-z0-9]+", "-", heading_match.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{text}</h{level}>')
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(
            r"^\|[\s\-:|]+\|$", lines[i + 1]
        ):
            header_cells = [
                _inline(c.strip()) for c in line.strip("|").split("|")
            ]
            out.append("<table>")
            out.append("<thead><tr>")
            for cell in header_cells:
                out.append(f"<th>{cell}</th>")
            out.append("</tr></thead>")
            out.append("<tbody>")
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                cells = [
                    _inline(c.strip()) for c in lines[i].strip("|").split("|")
                ]
                out.append("<tr>")
                for cell in cells:
                    out.append(f"<td>{cell}</td>")
                out.append("</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        if line.startswith("- ") or line.startswith("* "):
            out.append("<ul>")
            while i < len(lines) and (
                lines[i].startswith("- ") or lines[i].startswith("* ")
            ):
                out.append(f"<li>{_inline(lines[i][2:])}</li>")
                i += 1
            out.append("</ul>")
            continue

        if line.strip() == "":
            i += 1
            continue

        para_lines: list[str] = []
        while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith(
            "#"
        ) and not lines[i].startswith("```") and not lines[i].startswith("|") and not (
            lines[i].startswith("---") and all(c == "-" for c in lines[i].strip())
        ):
            para_lines.append(lines[i])
            i += 1
        out.append(f"<p>{_inline(' '.join(para_lines))}</p>")

    return "\n".join(out)


def _inline(text: str) -> str:
    """Convert inline Markdown formatting to HTML.

    Args:
        text: Raw inline Markdown text.

    Returns:
        HTML string with inline formatting applied.
    """
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"_([^_]+)_", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    return text


def _wrap_html(title: str, body: str, css_path: str | None = None) -> str:
    """Wrap HTML body content in a full page matching the site theme.

    Args:
        title: Page title.
        body: HTML body content.
        css_path: Relative path to the shared stylesheet, or None for inline.

    Returns:
        Complete HTML document string.
    """
    style_tag = (
        f'<link rel="stylesheet" href="{css_path}">'
        if css_path
        else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    {style_tag}
    <style>
        .md-content {{ max-width: 960px; margin: 0 auto; padding: 16px; }}
        .md-content table {{
            border-collapse: collapse; width: 100%; margin: 12px 0;
            font-size: 12px;
        }}
        .md-content th, .md-content td {{
            border: 1px solid var(--border);
            padding: 6px 10px; text-align: left;
        }}
        .md-content th {{
            background: var(--surface);
            font-weight: 600; font-size: 12px;
        }}
        .md-content pre {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            padding: 12px; border-radius: 4px;
            overflow-x: auto; margin: 10px 0;
        }}
        .md-content pre code {{
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 12px; line-height: 1.5;
            background: none; padding: 0; border-radius: 0;
        }}
        .md-content code {{
            background: var(--code-bg);
            padding: 1px 4px; border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 0.9em;
        }}
        .md-content hr {{
            border: 0; border-top: 1px solid var(--border);
            margin: 20px 0;
        }}
        .md-content h1 {{
            font-size: 18px; font-weight: 600;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px; margin-bottom: 16px;
        }}
        .md-content h2 {{
            font-size: 14px; font-weight: 600;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px; margin-top: 20px; margin-bottom: 10px;
        }}
        .md-content h3 {{
            font-size: 13px; font-weight: 600;
            margin-top: 16px; margin-bottom: 8px;
        }}
        .md-content p {{ font-size: 12px; margin-bottom: 8px; color: var(--text); }}
        .md-content ul {{ font-size: 12px; padding-left: 16px; margin: 8px 0; }}
        .md-content li {{ margin-bottom: 4px; }}
        .md-content strong {{ font-weight: 600; }}
        .nav-bar {{
            padding: 8px 16px;
            border-bottom: 1px solid var(--border);
            background: var(--surface);
        }}
        .nav-bar a {{
            color: var(--text-muted); text-decoration: none;
            margin-right: 16px; font-size: 12px;
        }}
        .nav-bar a:hover {{ color: var(--text); text-decoration: underline; }}
        .nav-bar a.active {{ color: var(--accent); font-weight: 600; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <button class="toolbar-btn" id="zoom-out-btn" title="Zoom out">&minus;</button>
        <span class="zoom-label" id="zoom-level">100%</span>
        <button class="toolbar-btn" id="zoom-in-btn" title="Zoom in">+</button>
        <div class="toolbar-divider"></div>
        <button class="toolbar-btn" id="theme-btn" title="Toggle theme">auto</button>
    </div>
    <nav class="nav-bar">
        <a href="index.html">Modules</a>
        <a href="mcp-server.html">MCP Server</a>
        <a href="cli.html">CLI</a>
    </nav>
    <div class="md-content">
        {body}
    </div>
    <script>
    (function() {{
        var currentZoom = 100;
        var container = document.querySelector('.md-content');
        var zoomLevel = document.getElementById('zoom-level');
        var zoomIn = document.getElementById('zoom-in-btn');
        var zoomOut = document.getElementById('zoom-out-btn');
        if (zoomIn) {{ zoomIn.onclick = function() {{
            if (currentZoom < 200) {{ currentZoom += 10; container.style.zoom = currentZoom / 100; zoomLevel.textContent = currentZoom + '%'; }}
        }}; }}
        if (zoomOut) {{ zoomOut.onclick = function() {{
            if (currentZoom > 50) {{ currentZoom -= 10; container.style.zoom = currentZoom / 100; zoomLevel.textContent = currentZoom + '%'; }}
        }}; }}
    }})();
    (function() {{
        var themes = ['auto', 'light', 'dark'];
        var prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        var currentSetting = 'auto';
        var themeBtn = document.getElementById('theme-btn');
        function resolveTheme(s) {{ return s === 'auto' ? (prefersDark.matches ? 'dark' : 'light') : s; }}
        function apply() {{
            document.documentElement.setAttribute('data-theme', resolveTheme(currentSetting));
            if (themeBtn) themeBtn.textContent = currentSetting;
        }}
        if (themeBtn) {{
            themeBtn.onclick = function() {{
                var idx = themes.indexOf(currentSetting);
                currentSetting = themes[(idx + 1) % themes.length];
                apply();
            }};
        }}
        prefersDark.addEventListener('change', function() {{ apply(); }});
        apply();
    }})();
    </script>
</body>
</html>"""


def main() -> None:
    """Parse arguments and convert Markdown files to HTML."""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to themed HTML pages",
    )
    parser.add_argument(
        "files", nargs="+", help="Markdown files to convert",
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="Output directory for HTML files",
    )
    parser.add_argument(
        "--css-path", default=None,
        help="Relative path to shared stylesheet",
    )
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    for md_path_str in args.files:
        md_path = Path(md_path_str)
        md_text = md_path.read_text()

        title_match = re.match(r"^#\s+(.*)", md_text)
        title = title_match.group(1) if title_match else md_path.stem

        body = _convert_markdown(md_text)
        page = _wrap_html(title, body, css_path=args.css_path)

        stem = md_path.stem
        if stem.startswith("12-"):
            out_name = "mcp-server.html"
        elif stem.startswith("13-"):
            out_name = "cli.html"
        else:
            out_name = f"{stem}.html"

        out_file = out_dir / out_name
        out_file.write_text(page)
        print(f"  {out_name}")


if __name__ == "__main__":
    main()
