#!/usr/bin/env python3
"""
Regenerate HTML pages from templates and metadata.

Usage:
    regenerate-pages.py all TEMPLATES_DIR METADATA_FILE OUTPUT_DIR REPO_URL
    regenerate-pages.py landing TEMPLATES_DIR METADATA_FILE OUTPUT_FILE REPO_URL
    regenerate-pages.py pr PR_NUMBER TEMPLATES_DIR METADATA_FILE OUTPUT_FILE

Arguments:
    all     - Regenerate landing page and all PR pages
    landing - Regenerate only landing page
    pr      - Regenerate specific PR page
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_template(template_path):
    """Load HTML template from file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_metadata(metadata_path):
    """Load PR metadata from JSON file."""
    if not metadata_path.exists():
        return {'prs': []}
    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_timestamp(iso_timestamp):
    """Format ISO timestamp to human-readable string."""
    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M UTC')


def generate_pr_list_html(prs):
    """Generate HTML table of PRs."""
    if not prs:
        return '<p>No pull requests with specification changes yet.</p>'

    html = ['<table>', '<thead>', '<tr>']
    html.append('<th>PR</th>')
    html.append('<th>Title</th>')
    html.append('<th>Status</th>')
    html.append('<th>Last Updated</th>')
    html.append('<th>Links</th>')
    html.extend(['</tr>', '</thead>', '<tbody>'])

    for pr in prs:
        status = pr['status']
        status_class = f"badge-{status}"
        status_text = status.capitalize()

        html.append('<tr>')
        html.append(f'<td><a href="{pr["pr_url"]}">#{pr["number"]}</a></td>')
        html.append(f'<td>{pr["title"]}</td>')
        html.append(f'<td><span class="badge {status_class}">{status_text}</span></td>')
        html.append(f'<td class="timestamp">{format_timestamp(pr["last_updated"])}</td>')

        # Links
        pr_dir = f'pr-{pr["number"]}'
        html.append('<td class="pr-links">')
        html.append(f'<a href="{pr_dir}/">View</a>')
        html.append(f'<a href="{pr_dir}/spec.html">Spec</a>')
        html.append(f'<a href="{pr_dir}/diff.html">Diff</a>')
        html.append(f'<a href="{pr["pr_url"]}">GitHub</a>')
        html.append('</td>')

        html.append('</tr>')

    html.extend(['</tbody>', '</table>'])
    return '\n'.join(html)


def generate_landing_page(template_path, metadata_path, output_path, repo_url):
    """Generate landing page from template and metadata."""
    template = load_template(template_path)
    data = load_metadata(metadata_path)

    pr_list_html = generate_pr_list_html(data['prs'])

    # Replace placeholders
    html = template.replace('{{REPO_URL}}', repo_url)
    html = html.replace('{{MAIN_SPEC_URL}}', 'main/spec.html')
    html = html.replace('{{PR_LIST}}', pr_list_html)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated landing page: {output_path}")


def generate_pr_page(pr_number, template_path, metadata_path, output_path):
    """Generate PR page from template and metadata."""
    template = load_template(template_path)
    data = load_metadata(metadata_path)

    # Find PR in metadata
    pr = None
    for p in data['prs']:
        if p['number'] == pr_number:
            pr = p
            break

    if not pr:
        print(f"Error: PR #{pr_number} not found in metadata", file=sys.stderr)
        sys.exit(1)

    # Replace placeholders
    html = template.replace('{{PR_NUMBER}}', str(pr['number']))
    html = html.replace('{{PR_TITLE}}', pr['title'])
    html = html.replace('{{PR_URL}}', pr['pr_url'])
    html = html.replace('{{REPO_URL}}', pr['repo_url'])
    html = html.replace('{{LANDING_URL}}', '../../index.html')
    html = html.replace('{{SPEC_URL}}', 'spec.html')
    html = html.replace('{{DIFF_URL}}', 'diff.html')

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated PR page: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: regenerate-pages.py {all|landing|pr} ...", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'landing':
        if len(sys.argv) != 6:
            print("Usage: regenerate-pages.py landing TEMPLATES_DIR METADATA_FILE OUTPUT_FILE REPO_URL", file=sys.stderr)
            sys.exit(1)

        templates_dir = Path(sys.argv[2])
        metadata_file = Path(sys.argv[3])
        output_file = Path(sys.argv[4])
        repo_url = sys.argv[5]

        template_path = templates_dir / 'landing.html'
        generate_landing_page(template_path, metadata_file, output_file, repo_url)

    elif command == 'pr':
        if len(sys.argv) != 6:
            print("Usage: regenerate-pages.py pr PR_NUMBER TEMPLATES_DIR METADATA_FILE OUTPUT_FILE", file=sys.stderr)
            sys.exit(1)

        pr_number = int(sys.argv[2])
        templates_dir = Path(sys.argv[3])
        metadata_file = Path(sys.argv[4])
        output_file = Path(sys.argv[5])

        template_path = templates_dir / 'pr.html'
        generate_pr_page(pr_number, template_path, metadata_file, output_file)

    elif command == 'all':
        if len(sys.argv) != 6:
            print("Usage: regenerate-pages.py all TEMPLATES_DIR METADATA_FILE OUTPUT_DIR REPO_URL", file=sys.stderr)
            sys.exit(1)

        templates_dir = Path(sys.argv[2])
        metadata_file = Path(sys.argv[3])
        output_dir = Path(sys.argv[4])
        repo_url = sys.argv[5]

        # Generate landing page
        landing_template = templates_dir / 'landing.html'
        landing_output = output_dir / 'index.html'
        generate_landing_page(landing_template, metadata_file, landing_output, repo_url)

        # Generate all PR pages
        data = load_metadata(metadata_file)
        pr_template = templates_dir / 'pr.html'

        for pr in data['prs']:
            pr_output = output_dir / f'pr-{pr["number"]}' / 'index.html'
            generate_pr_page(pr['number'], pr_template, metadata_file, pr_output)

    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
