#!/usr/bin/env python3
"""
Manage PR metadata in prs.json file.

Usage:
    manage-pr-metadata.py update PR_NUMBER TITLE STATUS PR_URL REPO_URL
    manage-pr-metadata.py close PR_NUMBER
    manage-pr-metadata.py merge PR_NUMBER

Arguments:
    update - Add or update a PR entry
    close  - Mark PR as closed
    merge  - Mark PR as merged
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_metadata(filepath):
    """Load existing metadata or create new structure."""
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'prs': []}


def save_metadata(filepath, data):
    """Save metadata to file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def find_pr(data, pr_number):
    """Find PR entry by number."""
    for i, pr in enumerate(data['prs']):
        if pr['number'] == pr_number:
            return i
    return None


def update_pr(filepath, pr_number, title, status, pr_url, repo_url):
    """Add or update a PR entry."""
    data = load_metadata(filepath)

    pr_entry = {
        'number': pr_number,
        'title': title,
        'status': status,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'spec_url': f'pr-{pr_number}/spec.html',
        'diff_url': f'pr-{pr_number}/diff.html',
        'pr_url': pr_url,
        'repo_url': repo_url
    }

    idx = find_pr(data, pr_number)
    if idx is not None:
        # Update existing entry (preserve status if not changed)
        if data['prs'][idx]['status'] in ['closed', 'merged'] and status == 'open':
            # Don't reopen closed/merged PRs unless explicitly set
            pr_entry['status'] = data['prs'][idx]['status']
        data['prs'][idx] = pr_entry
    else:
        # Add new entry
        data['prs'].append(pr_entry)

    # Sort by PR number descending (newest first)
    data['prs'].sort(key=lambda x: x['number'], reverse=True)

    save_metadata(filepath, data)
    print(f"Updated PR #{pr_number}: {title} ({status})")


def change_status(filepath, pr_number, new_status):
    """Change PR status to closed or merged."""
    data = load_metadata(filepath)

    idx = find_pr(data, pr_number)
    if idx is None:
        print(f"Error: PR #{pr_number} not found", file=sys.stderr)
        sys.exit(1)

    data['prs'][idx]['status'] = new_status
    data['prs'][idx]['last_updated'] = datetime.utcnow().isoformat() + 'Z'

    save_metadata(filepath, data)
    print(f"Marked PR #{pr_number} as {new_status}")


def main():
    if len(sys.argv) < 2:
        print("Usage: manage-pr-metadata.py {update|close|merge} ...", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    # Default metadata file location (can be overridden with env var)
    metadata_file = Path(sys.argv[-1] if sys.argv[-1].endswith('.json') else 'prs.json')

    if command == 'update':
        if len(sys.argv) != 7:
            print("Usage: manage-pr-metadata.py update PR_NUMBER TITLE STATUS PR_URL REPO_URL", file=sys.stderr)
            sys.exit(1)

        pr_number = int(sys.argv[2])
        title = sys.argv[3]
        status = sys.argv[4]
        pr_url = sys.argv[5]
        repo_url = sys.argv[6]

        update_pr(metadata_file, pr_number, title, status, pr_url, repo_url)

    elif command in ['close', 'merge']:
        if len(sys.argv) != 3:
            print(f"Usage: manage-pr-metadata.py {command} PR_NUMBER", file=sys.stderr)
            sys.exit(1)

        pr_number = int(sys.argv[2])
        change_status(metadata_file, pr_number, command + 'd')

    else:
        print(f"Error: Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
