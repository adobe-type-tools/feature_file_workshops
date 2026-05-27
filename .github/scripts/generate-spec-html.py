#!/usr/bin/env python3
"""
Generate HTML from markdown specification using GitHub's API.

Usage:
    generate-spec-html.py INPUT OUTPUT

Arguments:
    INPUT   - Path to markdown file
    OUTPUT  - Path to output HTML file
"""

import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# HTML template with GitHub styling
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OpenType Feature File Specification</title>
    <style>
/* GitHub Primer Base Styles */
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    color: #1f2328;
    background-color: #ffffff;
    margin: 0;
    padding: 20px;
    max-width: 980px;
    margin: 0 auto;
}}

/* PrettyLights Syntax Highlighting */
:root {{
    --color-prettylights-syntax-comment: #59636e;
    --color-prettylights-syntax-constant: #0550ae;
    --color-prettylights-syntax-entity: #6639ba;
    --color-prettylights-syntax-entity-tag: #0550ae;
    --color-prettylights-syntax-keyword: #cf222e;
    --color-prettylights-syntax-string: #0a3069;
    --color-prettylights-syntax-variable: #953800;
}}

.pl-c {{ color: var(--color-prettylights-syntax-comment); }}
.pl-c1, .pl-s .pl-v {{ color: var(--color-prettylights-syntax-constant); }}
.pl-e, .pl-en {{ color: var(--color-prettylights-syntax-entity); }}
.pl-ent {{ color: var(--color-prettylights-syntax-entity-tag); }}
.pl-k {{ color: var(--color-prettylights-syntax-keyword); }}
.pl-s {{ color: var(--color-prettylights-syntax-string); }}
.pl-v, .pl-smw {{ color: var(--color-prettylights-syntax-variable); }}

/* Code block styling */
pre {{
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
}}

code {{
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}}

pre code {{
    display: inline;
    padding: 0;
    margin: 0;
    background-color: transparent;
}}

/* Navigation link to return */
.nav-link {{
    display: block;
    margin-bottom: 20px;
    color: #0969da;
    text-decoration: none;
    font-size: 14px;
}}
.nav-link:hover {{
    text-decoration: underline;
}}
    </style>
</head>
<body>
{content}
</body>
</html>
'''


def sort_table_rows(html_content):
    """
    Sort the rows of every <tbody> by the text of the first cell.

    DaisyDiff diffs HTML linearly, so reordered table rows appear as a mass
    of interleaved additions and deletions even when the cell content is
    unchanged.  Sorting both the old and new HTML into the same order before
    diffing means only genuine cell-content changes (and truly new/removed
    rows) show as differences.

    The sort key is the text of the first <code> element inside the first
    <td>, which matches the keyword column in the spec tables.  Falls back
    to the plain text of the first <td> for tables that use a different
    structure.
    """

    def row_key(row_html):
        m = re.search(r'<td[^>]*>.*?<code[^>]*>([^<]+)</code>', row_html, re.DOTALL)
        if m:
            return m.group(1).lower()
        m = re.search(r'<td[^>]*>(.*?)</td>', row_html, re.DOTALL)
        if m:
            return re.sub(r'<[^>]+>', '', m.group(1)).strip().lower()
        return ''

    def sort_tbody(match):
        rows = re.findall(r'<tr>.*?</tr>', match.group(1), re.DOTALL)
        return '<tbody>' + ''.join(sorted(rows, key=row_key)) + '</tbody>'

    return re.sub(r'<tbody>(.*?)</tbody>', sort_tbody, html_content, flags=re.DOTALL)


def convert_markdown_to_html(markdown_content):
    """
    Convert markdown to HTML using GitHub's API.

    Args:
        markdown_content: String containing markdown content

    Returns:
        HTML string

    Raises:
        HTTPError: If GitHub API request fails
        URLError: If connection fails
    """
    url = 'https://api.github.com/markdown'
    payload = json.dumps({
        'text': markdown_content,
        'mode': 'gfm'
    }).encode('utf-8')

    headers = {
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json'
    }

    # Add authentication if GITHUB_TOKEN is available
    github_token = os.environ.get('GITHUB_TOKEN')
    if github_token:
        headers['Authorization'] = f'Bearer {github_token}'

    # Make request
    req = Request(url, data=payload, headers=headers, method='POST')
    with urlopen(req) as response:
        html = response.read().decode('utf-8')
        return html


def main():
    if len(sys.argv) != 3:
        print("Usage: generate-spec-html.py INPUT OUTPUT", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Read markdown
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert via GitHub API
        html_content = convert_markdown_to_html(markdown_content)

        # The GitHub API surrounds the content of every <pre> block with
        # whitespace: a newline + indentation before the first token, and a
        # newline + indentation before the closing tag.  Inside a <pre> that
        # whitespace renders as visible blank lines / indentation, so strip
        # both ends here before the file goes into DaisyDiff.
        html_content = re.sub(r'(<pre[^>]*>)\s+', r'\1', html_content)
        html_content = re.sub(r'\s+(</pre>)', r'\1', html_content)

        # Sort table rows so that DaisyDiff sees reordered rows as unchanged
        # rather than as interleaved additions and deletions.
        html_content = sort_table_rows(html_content)

        # Wrap in full HTML document
        full_html = HTML_TEMPLATE.format(content=html_content)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print(f"Generated: {output_path}")

    except HTTPError as e:
        print(f"Error: GitHub API request failed (HTTP {e.code})", file=sys.stderr)
        if e.code == 403:
            print("Hint: You may have hit the rate limit. Try setting GITHUB_TOKEN.", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Error: Could not connect to GitHub API: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
