#!/usr/bin/env python3
"""
Validate feature file examples using the ANTLR Python parser.

Usage:
    validate-examples                  # Validate all examples
    validate-examples path/to/file.fea # Validate specific file
    validate-examples -q               # Quiet mode (only show summary)
    validate-examples -h               # Show help
"""

import sys
import argparse
from pathlib import Path

# Set up paths
SCRIPT_DIR = Path(__file__).parent.resolve()
LIB_DIR = SCRIPT_DIR / 'lib'
PARSER_DIR = SCRIPT_DIR / 'grammar' / 'python_generated'

# Check dependencies exist
if not LIB_DIR.exists():
    print("\033[0;31mError: Dependencies not installed\033[0m", file=sys.stderr)
    print("\nPlease run setup first:", file=sys.stderr)
    print("  ./setup", file=sys.stderr)
    sys.exit(1)

if not PARSER_DIR.exists() or not (PARSER_DIR / 'FeatParser.py').exists():
    print("\033[0;31mError: Parser not generated\033[0m", file=sys.stderr)
    print("\nPlease run setup first:", file=sys.stderr)
    print("  ./setup", file=sys.stderr)
    sys.exit(1)

# Add lib/ and parser to path
sys.path.insert(0, str(LIB_DIR))
sys.path.insert(0, str(PARSER_DIR))

# Check if grammar files are stale (can be overridden with --force)
grammar_files = [
    SCRIPT_DIR / 'grammar' / 'FeatLexer.g4',
    SCRIPT_DIR / 'grammar' / 'FeatLexerPython.g4',
    SCRIPT_DIR / 'grammar' / 'FeatParser.g4'
]
parser_file = PARSER_DIR / 'FeatParser.py'

# Note: This check happens during import-time, so we need to check sys.argv directly
# (argparse hasn't run yet)
force_flag = '-f' in sys.argv or '--force' in sys.argv
help_flag = '-h' in sys.argv or '--help' in sys.argv

if not force_flag and not help_flag and any(g.stat().st_mtime > parser_file.stat().st_mtime for g in grammar_files if g.exists()):
    print("\033[0;31mWarning: Grammar files have been modified since parser was generated\033[0m", file=sys.stderr)
    print("\nPlease regenerate the parser:", file=sys.stderr)
    print("  ./setup", file=sys.stderr)
    print("\nOr use --force to validate with the current parser anyway.", file=sys.stderr)
    print()
    sys.exit(1)

# Import validator
from antlr4 import FileStream, CommonTokenStream
from FeatLexerPython import FeatLexerPython
from FeatParser import FeatParser
from antlr4.error.ErrorListener import ErrorListener


class FeatureFileErrorListener(ErrorListener):
    """Custom error listener for collecting parse errors."""

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append({
            'line': line if line else 0,
            'column': column if column else 0,
            'message': msg if msg else "Syntax error",
            'symbol': str(offendingSymbol.text) if offendingSymbol and hasattr(offendingSymbol, 'text') else None
        })


def validate_feature_file(filepath):
    """
    Parse feature file and return list of errors.

    Args:
        filepath: Path to .fea file

    Returns:
        List of error dictionaries with keys: line, column, message, symbol
    """
    try:
        input_stream = FileStream(str(filepath), encoding='utf-8')
    except Exception as e:
        return [{'line': 0, 'column': 0, 'message': f"Failed to read file: {e}", 'symbol': None}]

    # Create lexer
    lexer = FeatLexerPython(input_stream)
    stream = CommonTokenStream(lexer)

    # Create parser
    parser = FeatParser(stream)

    # Add custom error listener
    error_listener = FeatureFileErrorListener()
    parser.removeErrorListeners()  # Remove default console listener
    parser.addErrorListener(error_listener)

    # Parse the file
    try:
        parser.file_()
    except Exception as e:
        error_listener.errors.append({
            'line': 0,
            'column': 0,
            'message': f"Parse exception: {e}",
            'symbol': None
        })

    return error_listener.errors


def main():
    parser = argparse.ArgumentParser(
        description='Validate feature file examples using the ANTLR Python parser.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  validate-examples                  # Validate all examples
  validate-examples file.fea         # Validate specific file
  validate-examples -q               # Quiet mode (only show summary)
  validate-examples -f               # Force validation with stale parser
        """
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Feature file(s) to validate (default: all files in examples/)'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode: only show summary, suppress progress'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force validation even if grammar files are newer than parser'
    )

    args = parser.parse_args()

    if args.files:
        # Validate specific file(s)
        files = []
        for f in args.files:
            filepath = Path(f)
            if not filepath.exists():
                print(f"\033[0;31m❌ File not found: {filepath}\033[0m", file=sys.stderr)
                sys.exit(1)
            files.append(filepath)
    else:
        # Validate all examples
        files = sorted((SCRIPT_DIR / 'examples').rglob('*.fea'))
        if not files:
            print("\033[0;31mError: No .fea files found in examples/\033[0m", file=sys.stderr)
            sys.exit(1)

    passed = 0
    failed = 0
    failed_files = []

    # Validate each file
    for i, filepath in enumerate(files, 1):
        rel_path = filepath.relative_to(SCRIPT_DIR) if filepath.is_relative_to(SCRIPT_DIR) else filepath

        # Show progress (unless quiet)
        if not args.quiet:
            if len(files) > 1:
                print(f"[{i}/{len(files)}] Validating {rel_path}...", end='', flush=True)
            else:
                print(f"Validating {rel_path}...", end='', flush=True)

        errors = validate_feature_file(filepath)

        if errors:
            failed += 1
            failed_files.append((filepath, errors))

            if not args.quiet:
                print(f" \033[0;31m❌ FAILED\033[0m")

            # Print errors immediately
            for err in errors:
                location = f"  Line {err['line']}:{err['column']}" if err['line'] > 0 else "  File"
                print(f"{location} - {err['message']}")
                if err['symbol']:
                    print(f"    Near: {err['symbol']}")

            if not args.quiet:
                print()  # Blank line after errors
        else:
            passed += 1
            if not args.quiet:
                print(f" \033[0;32m✓\033[0m")

    # Print summary
    if not args.quiet:
        print()
    print("=" * 40)
    print(f"Results: \033[0;32m{passed} passed\033[0m, ", end='')
    if failed > 0:
        print(f"\033[0;31m{failed} failed\033[0m")
    else:
        print(f"{failed} failed")
    print("=" * 40)

    sys.exit(1 if failed > 0 else 0)


if __name__ == '__main__':
    main()
