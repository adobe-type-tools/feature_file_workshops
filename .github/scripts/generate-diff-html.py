#!/usr/bin/env python3
"""
Generate HTML diff between two HTML files using DaisyDiff.

Usage:
    generate-diff-html.py OLD_HTML NEW_HTML OUTPUT

Arguments:
    OLD_HTML - Path to old/base HTML file
    NEW_HTML - Path to new/modified HTML file
    OUTPUT   - Path to output diff HTML file
"""

import re
import subprocess
import sys
from pathlib import Path


def fix_asset_paths(html_file):
    """
    Post-process DaisyDiff output to fix asset paths and inject additional CSS.

    DaisyDiff generates relative paths like:
    - <link href="css/diff.css" ...>
    - <script src="js/diff.js" ...>

    We rewrite these to root-relative paths:
    - /assets/css/diff.css
    - /assets/js/diff.js

    Args:
        html_file: Path to the HTML file to modify
    """
    # Read the generated HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # DaisyDiff outputs bare-relative paths (css/, js/, images/).
    # Rewrite to paths relative to pr-{n}/diff.html on gh-pages.
    html_content = html_content.replace('href="css/', 'href="../assets/css/')
    html_content = html_content.replace('src="js/', 'src="../assets/js/')
    html_content = html_content.replace('src="images/', 'src="../assets/images/')

    # Inject additional CSS for GitHub Primer styling (before </head>)
    css_links = '''    <link rel="stylesheet" href="../assets/css/github-primer.css">
'''

    if '</head>' in html_content:
        html_content = html_content.replace('</head>', css_links + '</head>')
    else:
        # If no </head>, inject at beginning
        html_content = css_links + html_content

    # DaisyDiff re-introduces leading/trailing whitespace inside <pre> blocks
    # (a newline after the opening tag and before the closing tag), which
    # renders as blank lines in the browser.  Strip both ends.
    html_content = re.sub(r'(<pre[^>]*>)\s+', r'\1', html_content)
    html_content = re.sub(r'\s+(</pre>)', r'\1', html_content)

    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Fixed asset paths in {html_file}")


def main():
    if len(sys.argv) != 4:
        print("Usage: generate-diff-html.py OLD_HTML NEW_HTML OUTPUT", file=sys.stderr)
        sys.exit(1)

    old_html = Path(sys.argv[1])
    new_html = Path(sys.argv[2])
    output = Path(sys.argv[3])

    # Validate inputs
    if not old_html.exists():
        print(f"Error: Old HTML file not found: {old_html}", file=sys.stderr)
        sys.exit(1)

    if not new_html.exists():
        print(f"Error: New HTML file not found: {new_html}", file=sys.stderr)
        sys.exit(1)

    # Find DaisyDiff JAR
    script_dir = Path(__file__).parent.parent.parent  # Go up to repo root
    daisydiff_jar = script_dir / '.github' / 'daisydiff' / 'daisydiff-modified.jar'

    if not daisydiff_jar.exists():
        print(f"Error: DaisyDiff JAR not found: {daisydiff_jar}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Run DaisyDiff
        # Usage: java -jar daisydiff.jar [old.html] [new.html] [output.html]
        result = subprocess.run(
            [
                'java', '-jar', str(daisydiff_jar),
                str(old_html),
                str(new_html),
                '--file=' + str(output)
            ],
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Generated diff: {output}")

        # Show any warnings/info from DaisyDiff
        if result.stdout:
            print(result.stdout)

        # Post-process: fix asset paths and inject additional CSS
        fix_asset_paths(output)

    except subprocess.CalledProcessError as e:
        print(f"Error: DaisyDiff failed with exit code {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"Output: {e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
