#!/usr/bin/env python3
"""
Generate HTML preview of the specification using GitHub's markdown API.

Usage:
    ./generate-spec-preview.py                                  # Generate from OpenTypeFeatureFileSpecification.md
    ./generate-spec-preview.py path/to/spec.md                  # Generate from specific file
    ./generate-spec-preview.py path/to/spec.md output.html      # Specify output file
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# Terminal colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color


# HTML template with GitHub styling
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>OpenType Feature File Specification - Preview</title>
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
    </style>
</head>
<body>
{content}
</body>
</html>
'''


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
    parser = argparse.ArgumentParser(
        description='Generate HTML preview of the specification using GitHub\'s markdown API.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  ./generate-spec-preview.py                         # Use default spec file
  ./generate-spec-preview.py custom.md               # Convert custom file
  ./generate-spec-preview.py spec.md output.html     # Specify output
        """
    )

    script_dir = Path(__file__).parent.resolve()
    default_input = script_dir / 'OpenTypeFeatureFileSpecification.md'

    parser.add_argument(
        'input',
        nargs='?',
        default=str(default_input),
        help=f'Input markdown file (default: {default_input.name})'
    )
    parser.add_argument(
        'output',
        nargs='?',
        help='Output HTML file (default: input filename with .html extension)'
    )

    args = parser.parse_args()

    # Resolve paths
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"{RED}Error: Input file not found: {input_path}{NC}", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix('.html')

    # Show what we're doing
    print(f"{GREEN}Generating HTML preview...{NC}")
    print(f"  Input:  {input_path}")
    print(f"  Output: {output_path}")
    print()

    try:
        # Read markdown
        print("Converting markdown to HTML...")
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert via GitHub API
        html_content = convert_markdown_to_html(markdown_content)

        # Wrap in full HTML document
        full_html = HTML_TEMPLATE.format(content=html_content)

        # Write output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        print()
        print(f"{GREEN}✅ Preview generated: {output_path}{NC}")
        print()
        print("Open it in your browser:")
        print(f"  open {output_path}")

    except HTTPError as e:
        print(f"{RED}Error: GitHub API request failed (HTTP {e.code}){NC}", file=sys.stderr)
        if e.code == 403:
            print(f"{YELLOW}Hint: You may have hit the rate limit. Try setting GITHUB_TOKEN.{NC}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"{RED}Error: Could not connect to GitHub API: {e.reason}{NC}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{RED}Error: {e}{NC}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
