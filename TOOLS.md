# Tools and Development Setup

This repository includes two sets of tools to make it easier to test and review
changes to the specification. Both sets of tools execute on each PR as part of
our GitHub CI, but we have also tried to make it easy to run them locally.

## HTML Specification Preview

The `generate-spec-preview.py` script converts the Markdown specification to
GitHub-styled HTML. It uses Python's standard library to call GitHub's
markdown rendering API, requiring no additional dependencies.

**Generate preview:**
```bash
./generate-spec-preview.py
```

This creates `OpenTypeFeatureFileSpecification.html` in the current directory.

Run `./generate-spec-preview.py --help` for more options.

## Feature file example validator

The `examples` directory contains feature files that exercise various parts of
the specification. Each of these should be parsable by the Antlr4 grammar
specified in the `grammar` directory. The `.g4` files in that directory are
very close to those Adobe uses in the AFDKO toolset. Ideally, PR submitters
who are proposing grammar changes will add them to the Antlr4 grammar and also
add examples that exercise the new or changed functionality.

### Prerequisites

#### Required Software

1. **Python 3.7+**
   ```bash
   python3 --version  # Check your version
   ```

2. **Java 11+** (for ANTLR parser generation)
   ```bash
   java -version  # Check your version
   ```

#### Python Dependencies

Python dependencies are automatically installed to a local `lib/` directory by
the setup script, keeping your system Python environment clean.

## Quick Start

The `setup.py` script handles all setup automatically:

```bash
./setup.py
```

This will:
1. Check that Java 11+ and Python 3.7+ are available
2. Install Python dependencies to `lib/` directory (no system pollution)
3. Generate the ANTLR parser from grammar files

**You need to run setup:**
- When you first clone the repository
- After modifying any grammar files (`FeatLexer.g4`, `FeatLexerPython.g4`, or `FeatParser.g4`)

## Using the Tools

### Validating Feature Files

The `validate-examples.py` script validates feature files using the ANTLR Python parser.

**Validate all examples:**
```bash
./validate-examples.py
```

Output:
```
[1/76] Validating examples/advanced/anonymous_block.fea... ✓
[2/76] Validating examples/advanced/cvParameters.fea... ✓
[3/76] Validating examples/advanced/featureNames.fea... ✓
...
[76/76] Validating examples/tables/vhea_metrics.fea... ✓

========================================
Results: 76 passed, 0 failed
========================================
```

**Validate specific file(s):**
```bash
./validate-examples.py examples/features/ligatures.fea
./validate-examples.py file1.fea file2.fea file3.fea
```

**Quiet mode (only show summary):**
```bash
./validate-examples.py -q
```

**Force validation with stale parser:**
```bash
./validate-examples.py -f
# or
./validate-examples.py --force
```

If you've modified grammar files but want to validate examples without
regenerating the parser, use `--force` to skip the stale parser check.

**Show help:**
```bash
./validate-examples.py -h
```

**What it checks:**
- Syntax errors (grammar violations)
- Parse errors (structure issues)
- Token recognition problems

**What it doesn't check:**
- Semantic correctness (e.g., undefined glyph references)
- Runtime behavior
- Font compilation

**Error output:**

When validation fails, errors are shown immediately with line/column information:

```
[15/76] Validating examples/bad/syntax_error.fea... ❌ FAILED
  Line 5:10 - mismatched input ';' expecting '}'
    Near: ;

[16/76] Validating examples/basic/glyphclass.fea... ✓
```

## Repository Structure

```
.
├── .github/
│   ├── workflows/          # CI workflows
│   ├── requirements.txt    # Python dependencies (just antlr4-python3-runtime)
│   ├── antlr-4.13.2-complete.jar  # ANTLR tool
│   ├── daisydiff/          # Modified DaisyDiff JAR for HTML diffs
│   └── diff-generation/    # Scripts for generating PR diffs
│
├── grammar/
│   ├── FeatLexer.g4        # Core lexer (edit this)
│   ├── FeatLexerPython.g4  # Python wrapper with anonymous block support
│   ├── FeatParser.g4       # Parser rules (edit this)
│   └── python_generated/   # Generated parser (gitignored)
│
├── examples/               # Example feature files
├── lib/                   # Local Python dependencies (gitignored)
├── tools/
│   └── validator/         # Validator implementation
│
├── setup.py                  # Setup script (install deps, generate parser)
├── validate-examples.py      # Validate feature files
└── generate-spec-preview.py  # Generate HTML preview of spec
```

## For Contributors

### Modifying Grammar Files

If you're proposing changes to the grammar:

1. Edit `grammar/FeatLexer.g4` or `grammar/FeatParser.g4`
2. Run `./setup.py` to regenerate the parser
3. Add or modify examples in `examples/` to demonstrate the new syntax
4. Run `./validate-examples.py` to ensure all examples still parse
5. Submit your PR with both grammar changes and example files

The CI will automatically:
- Regenerate the parser from your grammar changes
- Validate all examples
- Generate a visual diff of the specification (if you modified the markdown)

### Stale Parser Detection

The `validate-examples.py` script checks if grammar files are newer than the
generated parser and warns you:

```
Warning: Grammar files have been modified since parser was generated

Please regenerate the parser:
  ./setup.py
```

This ensures you're always testing with the current grammar.

## Troubleshooting

### "Error: Dependencies not installed"

Run `./setup.py` to install dependencies and generate the parser.

### "Error: Java 11+ required"

ANTLR 4.13.2 requires Java 11 or later. Check your Java version:

```bash
java -version
```

If you have Java 8 or older, you'll need to install Java 11+. On macOS with Homebrew:

```bash
brew install openjdk@11
export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"
```

### Parser warnings during generation

When `setup.py` generates the parser, you may see warnings like:

```
warning(155): FeatParser.g4:47:0: rule file contains an optional block with at least one alternative that can match an empty string
```

These warnings are normal and expected. They come from ANTLR analyzing the
grammar and do not indicate errors.

### GitHub API rate limits

`generate-spec-preview.py` uses GitHub's markdown API which has rate limits:
- 60 requests/hour without authentication
- 5000 requests/hour with a GitHub token

If you hit the limit, either wait an hour or set up authentication:

```bash
export GITHUB_TOKEN="your_github_token"
./generate-spec-preview.py
```

## CI Workflows

When you submit a PR, GitHub Actions automatically:

1. **Validate Examples** (`.github/workflows/validate-examples.yml`)
   - Checks if grammar files changed
   - Regenerates parser if needed
   - Validates all example files
   - Reports any parsing errors

2. **Generate Spec Diff** (future - not yet implemented)
   - Generates HTML from current and previous spec versions
   - Creates visual diff showing changes
   - Publishes to GitHub Pages for review

You can see the CI configuration in `.github/workflows/`.
