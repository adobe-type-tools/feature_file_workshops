#!/usr/bin/env bash
#
# Generate HTML diff using GitHub's markdown API with prettylights syntax highlighting
#
# This script:
# 1. Converts markdown to HTML using GitHub's API
# 2. Normalizes article IDs for proper section matching
# 3. Runs modified DaisyDiff (with code block preservation)
# 4. Generates full diff view
#

set -euo pipefail

# Default values
KEEP_TEMP=false
VERBOSE=false

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS] OLD_SPEC NEW_SPEC OUTPUT

Generate HTML diff using GitHub's markdown API.

Arguments:
  OLD_SPEC    Path to old version of specification (markdown)
  NEW_SPEC    Path to new version of specification (markdown)
  OUTPUT      Path for output HTML file

Options:
  --keep-temp        Keep temporary files for debugging
  --verbose          Show detailed output
  -h, --help         Show this help message

Requirements:
  - curl
  - Python 3
  - Java 8 or later
  - Modified DaisyDiff JAR
EOF
}

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-temp)
            KEEP_TEMP=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# Restore positional parameters
set -- "${POSITIONAL_ARGS[@]}"

# Validate arguments
if [[ $# -ne 3 ]]; then
    log_error "Expected 3 arguments, got $#"
    usage
    exit 1
fi

OLD_SPEC="$1"
NEW_SPEC="$2"
OUTPUT="$3"

# Check input files exist
if [[ ! -f "$OLD_SPEC" ]]; then
    log_error "Old spec not found: $OLD_SPEC"
    exit 1
fi

if [[ ! -f "$NEW_SPEC" ]]; then
    log_error "New spec not found: $NEW_SPEC"
    exit 1
fi

# Check dependencies
if ! command -v curl &> /dev/null; then
    log_error "curl not found"
    exit 1
fi

if ! command -v java &> /dev/null; then
    log_error "Java not found. Please install Java 8 or later."
    exit 1
fi

# Find DaisyDiff JAR (relative to script location)
DAISYDIFF_JAR="$SCRIPT_DIR/../daisydiff/daisydiff-modified.jar"

if [[ ! -f "$DAISYDIFF_JAR" ]]; then
    # Try alternative locations
    for loc in \
        ".github/daisydiff/daisydiff-modified.jar" \
        "./.github/daisydiff/daisydiff-modified.jar" \
        "../.github/daisydiff/daisydiff-modified.jar"; do
        if [[ -f "$loc" ]]; then
            DAISYDIFF_JAR="$loc"
            break
        fi
    done
fi

if [[ ! -f "$DAISYDIFF_JAR" ]]; then
    log_error "Modified DaisyDiff JAR not found"
    log_error "Expected at: $SCRIPT_DIR/../daisydiff/daisydiff-modified.jar"
    exit 1
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
if [[ "$KEEP_TEMP" == "false" ]]; then
    trap "rm -rf '$TEMP_DIR'" EXIT
fi

[[ "$VERBOSE" == "true" ]] && log_info "Temporary directory: $TEMP_DIR"

# Step 1: Convert markdown to HTML using GitHub API
log_info "Converting markdown to HTML using GitHub API..."

convert_markdown_to_html() {
    local markdown_file="$1"
    local output_html="$2"

    # Read markdown content
    local markdown_content=$(cat "$markdown_file")

    # Escape for JSON (preserve newlines and quotes)
    local json_payload=$(python3 -c "
import json
import sys

with open('$markdown_file', 'r', encoding='utf-8') as f:
    content = f.read()

payload = {
    'text': content,
    'mode': 'gfm'
}
print(json.dumps(payload))
")

    # Call GitHub API (with authentication if GITHUB_TOKEN is available)
    local auth_header=""
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
        auth_header="-H \"Authorization: Bearer $GITHUB_TOKEN\""
    fi

    local response=$(curl -s -X POST \
        -H "Accept: application/vnd.github+json" \
        -H "Content-Type: application/json" \
        $auth_header \
        https://api.github.com/markdown \
        -d "$json_payload")

    # Wrap in HTML document with prettylights CSS
    cat > "$output_html" << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Spec Diff</title>
    <style>
/* GitHub Primer Base Styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.5;
    color: #1f2328;
    background-color: #ffffff;
    margin: 0;
    padding: 20px;
}

/* PrettyLights Syntax Highlighting - Color Definitions */
:root {
    --color-prettylights-syntax-comment: #59636e;
    --color-prettylights-syntax-constant: #0550ae;
    --color-prettylights-syntax-constant-other-reference-link: #0a3069;
    --color-prettylights-syntax-entity: #6639ba;
    --color-prettylights-syntax-entity-tag: #0550ae;
    --color-prettylights-syntax-invalid-illegal-text: #d1242f;
    --color-prettylights-syntax-invalid-illegal-bg: #ffebe9;
    --color-prettylights-syntax-keyword: #cf222e;
    --color-prettylights-syntax-markup-bold: #1f2328;
    --color-prettylights-syntax-markup-changed-bg: #ffd8b5;
    --color-prettylights-syntax-markup-changed-text: #953800;
    --color-prettylights-syntax-markup-deleted-bg: #ffebe9;
    --color-prettylights-syntax-markup-deleted-text: #82071e;
    --color-prettylights-syntax-markup-heading: #0550ae;
    --color-prettylights-syntax-markup-ignored-bg: #0550ae;
    --color-prettylights-syntax-markup-ignored-text: #d1d9e0;
    --color-prettylights-syntax-markup-inserted-bg: #dafbe1;
    --color-prettylights-syntax-markup-inserted-text: #116329;
    --color-prettylights-syntax-markup-italic: #1f2328;
    --color-prettylights-syntax-markup-list: #3b2300;
    --color-prettylights-syntax-meta-diff-range: #8250df;
    --color-prettylights-syntax-storage-modifier-import: #1f2328;
    --color-prettylights-syntax-string: #0a3069;
    --color-prettylights-syntax-string-regexp: #116329;
    --color-prettylights-syntax-sublimelinter-gutter-mark: #818b98;
    --color-prettylights-syntax-variable: #953800;
    --color-prettylights-syntax-brackethighlighter-angle: #59636e;
    --color-prettylights-syntax-brackethighlighter-unmatched: #82071e;
    --color-prettylights-syntax-carriage-return-bg: #cf222e;
    --color-prettylights-syntax-carriage-return-text: #f6f8fa;
}

/* PrettyLights Syntax Highlighting - Class Rules */
.pl-c { color: var(--color-prettylights-syntax-comment); }
.pl-c1, .pl-s .pl-v { color: var(--color-prettylights-syntax-constant); }
.pl-e, .pl-en { color: var(--color-prettylights-syntax-entity); }
.pl-smi, .pl-s .pl-s1 { color: var(--color-prettylights-syntax-storage-modifier-import); }
.pl-ent { color: var(--color-prettylights-syntax-entity-tag); }
.pl-k { color: var(--color-prettylights-syntax-keyword); }
.pl-s, .pl-pds, .pl-s .pl-pse .pl-s1, .pl-sr, .pl-sr .pl-cce, .pl-sr .pl-sre, .pl-sr .pl-sra {
    color: var(--color-prettylights-syntax-string);
}
.pl-v, .pl-smw { color: var(--color-prettylights-syntax-variable); }
.pl-bu { color: var(--color-prettylights-syntax-brackethighlighter-unmatched); }
.pl-ii {
    color: var(--color-prettylights-syntax-invalid-illegal-text);
    background-color: var(--color-prettylights-syntax-invalid-illegal-bg);
}
.pl-c2 {
    color: var(--color-prettylights-syntax-carriage-return-text);
    background-color: var(--color-prettylights-syntax-carriage-return-bg);
}
.pl-c2:before { content: "^M"; }
.pl-sr .pl-cce {
    color: var(--color-prettylights-syntax-string-regexp);
    font-weight: 700;
}
.pl-ml { color: var(--color-prettylights-syntax-markup-list); }
.pl-mh, .pl-mh .pl-en, .pl-ms {
    color: var(--color-prettylights-syntax-markup-heading);
    font-weight: 700;
}
.pl-mi {
    color: var(--color-prettylights-syntax-markup-italic);
    font-style: italic;
}
.pl-mb {
    color: var(--color-prettylights-syntax-markup-bold);
    font-weight: 700;
}
.pl-md {
    color: var(--color-prettylights-syntax-markup-deleted-text);
    background-color: var(--color-prettylights-syntax-markup-deleted-bg);
}
.pl-mi1 {
    color: var(--color-prettylights-syntax-markup-inserted-text);
    background-color: var(--color-prettylights-syntax-markup-inserted-bg);
}
.pl-mc {
    color: var(--color-prettylights-syntax-markup-changed-text);
    background-color: var(--color-prettylights-syntax-markup-changed-bg);
}
.pl-mi2 {
    color: var(--color-prettylights-syntax-markup-ignored-text);
    background-color: var(--color-prettylights-syntax-markup-ignored-bg);
}
.pl-mdr {
    color: var(--color-prettylights-syntax-meta-diff-range);
    font-weight: 700;
}
.pl-ba { color: var(--color-prettylights-syntax-brackethighlighter-angle); }
.pl-sg { color: var(--color-prettylights-syntax-sublimelinter-gutter-mark); }
.pl-corl {
    color: var(--color-prettylights-syntax-constant-other-reference-link);
    text-decoration: underline;
}

/* Code block styling */
pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
}

code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
}

pre code {
    display: inline;
    padding: 0;
    margin: 0;
    overflow: visible;
    line-height: inherit;
    word-wrap: normal;
    background-color: transparent;
    border: 0;
}

.highlight {
    margin-bottom: 16px;
}
    </style>
</head>
<body>
HTMLEOF

    echo "$response" >> "$output_html"

    cat >> "$output_html" << 'HTMLEOF'
</body>
</html>
HTMLEOF
}

OLD_HTML="$TEMP_DIR/old.html"
NEW_HTML="$TEMP_DIR/new.html"

convert_markdown_to_html "$OLD_SPEC" "$OLD_HTML"
convert_markdown_to_html "$NEW_SPEC" "$NEW_HTML"

# Step 2: Fix TOC links to match GitHub's anchor naming
log_info "Fixing table of contents links..."

python3 << PYTHON_EOF
import re

def fix_toc_links(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # GitHub API converts <a name="1"> to <a name="user-content-1">
    # But TOC links remain as href="#1"
    # Fix TOC links by adding the user-content- prefix
    # Pattern matches section IDs: 1, 2.a, 6.b.iii, 2.e.iia, etc.
    # Match: digit at start, then any combo of digits, lowercase letters, dots, roman 'i'
    content = re.sub(
        r'href="#([0-9]+(?:[a-z.i]+)?)"',
        r'href="#user-content-\1"',
        content
    )

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)

fix_toc_links("$OLD_HTML")
fix_toc_links("$NEW_HTML")
PYTHON_EOF

# Step 3: Normalize article IDs for proper section matching
log_info "Normalizing article IDs..."

OLD_NORM="$TEMP_DIR/old-normalized.html"
NEW_NORM="$TEMP_DIR/new-normalized.html"

# Replace dynamic article IDs with fixed ID
sed 's/id="user-content-article-[^"]*"/id="user-content-article"/g' "$OLD_HTML" > "$OLD_NORM"
sed 's/id="user-content-article-[^"]*"/id="user-content-article"/g' "$NEW_HTML" > "$NEW_NORM"

# Step 4: Run DaisyDiff
log_info "Generating diff with DaisyDiff..."

DIFF_OUTPUT="$TEMP_DIR/diff-raw.html"

if [[ "$VERBOSE" == "true" ]]; then
    java -jar "$DAISYDIFF_JAR" "$OLD_NORM" "$NEW_NORM" --file="$DIFF_OUTPUT"
else
    java -jar "$DAISYDIFF_JAR" "$OLD_NORM" "$NEW_NORM" --file="$DIFF_OUTPUT" 2>&1 | grep -v "^Comparing\|^Diff type\|^Writing\|^\.\.\.\.done$" || true
fi

# Step 5: Inject prettylights CSS into DaisyDiff output
log_info "Injecting prettylights CSS..."

python3 << PYTHON_EOF
import sys
import re

diff_file = "$DIFF_OUTPUT"
output_file = "$OUTPUT"

# Read DaisyDiff output
with open(diff_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Prettylights CSS to inject
prettylights_css = '''
/* PrettyLights Syntax Highlighting - Color Definitions */
:root {
    --color-prettylights-syntax-comment: #59636e;
    --color-prettylights-syntax-constant: #0550ae;
    --color-prettylights-syntax-constant-other-reference-link: #0a3069;
    --color-prettylights-syntax-entity: #6639ba;
    --color-prettylights-syntax-entity-tag: #0550ae;
    --color-prettylights-syntax-invalid-illegal-text: #d1242f;
    --color-prettylights-syntax-invalid-illegal-bg: #ffebe9;
    --color-prettylights-syntax-keyword: #cf222e;
    --color-prettylights-syntax-markup-bold: #1f2328;
    --color-prettylights-syntax-markup-changed-bg: #ffd8b5;
    --color-prettylights-syntax-markup-changed-text: #953800;
    --color-prettylights-syntax-markup-deleted-bg: #ffebe9;
    --color-prettylights-syntax-markup-deleted-text: #82071e;
    --color-prettylights-syntax-markup-heading: #0550ae;
    --color-prettylights-syntax-markup-ignored-bg: #0550ae;
    --color-prettylights-syntax-markup-ignored-text: #d1d9e0;
    --color-prettylights-syntax-markup-inserted-bg: #dafbe1;
    --color-prettylights-syntax-markup-inserted-text: #116329;
    --color-prettylights-syntax-markup-italic: #1f2328;
    --color-prettylights-syntax-markup-list: #3b2300;
    --color-prettylights-syntax-meta-diff-range: #8250df;
    --color-prettylights-syntax-storage-modifier-import: #1f2328;
    --color-prettylights-syntax-string: #0a3069;
    --color-prettylights-syntax-string-regexp: #116329;
    --color-prettylights-syntax-sublimelinter-gutter-mark: #818b98;
    --color-prettylights-syntax-variable: #953800;
    --color-prettylights-syntax-brackethighlighter-angle: #59636e;
    --color-prettylights-syntax-brackethighlighter-unmatched: #82071e;
    --color-prettylights-syntax-carriage-return-bg: #cf222e;
    --color-prettylights-syntax-carriage-return-text: #f6f8fa;
}

/* PrettyLights Syntax Highlighting - Class Rules */
.pl-c { color: var(--color-prettylights-syntax-comment); }
.pl-c1, .pl-s .pl-v { color: var(--color-prettylights-syntax-constant); }
.pl-e, .pl-en { color: var(--color-prettylights-syntax-entity); }
.pl-smi, .pl-s .pl-s1 { color: var(--color-prettylights-syntax-storage-modifier-import); }
.pl-ent { color: var(--color-prettylights-syntax-entity-tag); }
.pl-k { color: var(--color-prettylights-syntax-keyword); }
.pl-s, .pl-pds, .pl-s .pl-pse .pl-s1, .pl-sr, .pl-sr .pl-cce, .pl-sr .pl-sre, .pl-sr .pl-sra {
    color: var(--color-prettylights-syntax-string);
}
.pl-v, .pl-smw { color: var(--color-prettylights-syntax-variable); }
.pl-bu { color: var(--color-prettylights-syntax-brackethighlighter-unmatched); }
.pl-ii {
    color: var(--color-prettylights-syntax-invalid-illegal-text);
    background-color: var(--color-prettylights-syntax-invalid-illegal-bg);
}
.pl-c2 {
    color: var(--color-prettylights-syntax-carriage-return-text);
    background-color: var(--color-prettylights-syntax-carriage-return-bg);
}
.pl-c2:before { content: "^M"; }
.pl-sr .pl-cce {
    color: var(--color-prettylights-syntax-string-regexp);
    font-weight: 700;
}
.pl-ml { color: var(--color-prettylights-syntax-markup-list); }
.pl-mh, .pl-mh .pl-en, .pl-ms {
    color: var(--color-prettylights-syntax-markup-heading);
    font-weight: 700;
}
.pl-mi {
    color: var(--color-prettylights-syntax-markup-italic);
    font-style: italic;
}
.pl-mb {
    color: var(--color-prettylights-syntax-markup-bold);
    font-weight: 700;
}
.pl-md {
    color: var(--color-prettylights-syntax-markup-deleted-text);
    background-color: var(--color-prettylights-syntax-markup-deleted-bg);
}
.pl-mi1 {
    color: var(--color-prettylights-syntax-markup-inserted-text);
    background-color: var(--color-prettylights-syntax-markup-inserted-bg);
}
.pl-mc {
    color: var(--color-prettylights-syntax-markup-changed-text);
    background-color: var(--color-prettylights-syntax-markup-changed-bg);
}
.pl-mi2 {
    color: var(--color-prettylights-syntax-markup-ignored-text);
    background-color: var(--color-prettylights-syntax-markup-ignored-bg);
}
.pl-mdr {
    color: var(--color-prettylights-syntax-meta-diff-range);
    font-weight: 700;
}
.pl-ba { color: var(--color-prettylights-syntax-brackethighlighter-angle); }
.pl-sg { color: var(--color-prettylights-syntax-sublimelinter-gutter-mark); }
.pl-corl {
    color: var(--color-prettylights-syntax-constant-other-reference-link);
    text-decoration: underline;
}

/* Code block styling */
pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
}

code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
}

pre code {
    display: inline;
    padding: 0;
    margin: 0;
    overflow: visible;
    line-height: inherit;
    word-wrap: normal;
    background-color: transparent;
    border: 0;
}

.highlight {
    margin-bottom: 16px;
}
'''

# Inject CSS after </head> tag, or before </head> if it exists
if '</head>' in content:
    content = content.replace('</head>', '<style>\n' + prettylights_css + '\n</style>\n</head>')
else:
    # Fallback: add style tag after opening body tag
    content = content.replace('<body>', '<body>\n<style>\n' + prettylights_css + '\n</style>')

# Write output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Prettylights CSS injected successfully")
PYTHON_EOF

# Step 6: Copy DaisyDiff assets (css, js, images) alongside output
log_info "Copying DaisyDiff assets for navigation..."

OUTPUT_DIR=$(dirname "$OUTPUT")
DAISYDIFF_ASSETS="$SCRIPT_DIR/../daisydiff/assets"

if [[ -d "$DAISYDIFF_ASSETS" ]]; then
    # Copy css, js, and images directories
    for asset_dir in css js images; do
        if [[ -d "$DAISYDIFF_ASSETS/$asset_dir" ]]; then
            cp -r "$DAISYDIFF_ASSETS/$asset_dir" "$OUTPUT_DIR/" 2>/dev/null || true
        fi
    done
    [[ "$VERBOSE" == "true" ]] && log_info "Copied DaisyDiff assets to $OUTPUT_DIR"
else
    log_warn "DaisyDiff assets not found at $DAISYDIFF_ASSETS"
    log_warn "Arrow key navigation will not work (click navigation still works)"
fi

# Success message
log_info "Diff generated successfully: $OUTPUT"

if [[ "$KEEP_TEMP" == "true" ]]; then
    log_info "Temporary files kept at: $TEMP_DIR"
fi

# Display file size
SIZE=$(du -h "$OUTPUT" | cut -f1)
log_info "Output size: $SIZE"
