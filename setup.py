#!/usr/bin/env python3
"""
Setup script for Feature File Workshop tools.

This script:
1. Checks prerequisites (Java 11+, Python 3.7+)
2. Installs Python dependencies to local lib/ directory
3. Generates ANTLR parser from grammar files
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


# Terminal colors
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color


def print_color(msg, color=''):
    """Print colored message."""
    print(f"{color}{msg}{NC}")


def check_command(cmd):
    """Check if command exists in PATH."""
    return shutil.which(cmd) is not None


def get_java_version():
    """
    Get Java version number.

    Returns:
        int: Major version number (e.g., 8, 11, 17)

    Raises:
        RuntimeError: If Java not found or version can't be parsed
    """
    if not check_command('java'):
        raise RuntimeError("Java not found")

    try:
        # java -version outputs to stderr
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True,
            check=True
        )
        version_output = result.stderr

        # Parse version from first line: java version "1.8.0_421" or java version "11.0.1"
        match = re.search(r'"([^"]+)"', version_output.split('\n')[0])
        if not match:
            raise RuntimeError("Could not parse Java version")

        version_string = match.group(1)

        # Handle old format: 1.8.0_421 -> 8
        if version_string.startswith('1.'):
            old_match = re.match(r'1\.(\d+)', version_string)
            if old_match:
                return int(old_match.group(1))

        # Handle new format: 11.0.1 -> 11
        new_match = re.match(r'(\d+)', version_string)
        if new_match:
            return int(new_match.group(1))

        raise RuntimeError(f"Could not parse Java version from: {version_string}")

    except subprocess.CalledProcessError:
        raise RuntimeError("Failed to run java -version")


def main():
    script_dir = Path(__file__).parent.resolve()

    print_color("Setting up Feature File Workshop tools...", BLUE)
    print()

    # Check prerequisites
    print("Checking prerequisites...")

    # Check Java
    try:
        java_version = get_java_version()
        if java_version < 11:
            print_color(f"Error: Java 11+ required for ANTLR 4.13.2 (found Java {java_version})", RED)
            print("Install: https://www.oracle.com/java/technologies/downloads/")
            print()
            print("On macOS with Homebrew:")
            print("  brew install openjdk@11")
            print('  export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"')
            sys.exit(1)
        print_color(f"✓ Java {java_version}", GREEN)
    except RuntimeError as e:
        print_color(f"Error: {e}", RED)
        print("Java 11+ is required to run ANTLR")
        print("Install: https://www.oracle.com/java/technologies/downloads/")
        sys.exit(1)

    # Check Python (we're already running in Python, just show version)
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info < (3, 7):
        print_color(f"Error: Python 3.7+ required (found Python {python_version})", RED)
        sys.exit(1)
    print_color(f"✓ Python {python_version}", GREEN)

    # Check ANTLR JAR
    antlr_jar = script_dir / '.github' / 'antlr-4.13.2-complete.jar'
    if not antlr_jar.exists():
        print_color("Error: ANTLR JAR not found", RED)
        print(f"Expected at: {antlr_jar}")
        sys.exit(1)
    print_color("✓ ANTLR 4.13.2", GREEN)

    print()
    print("Installing Python dependencies...")

    # Install to local lib/ directory (no venv needed)
    lib_dir = script_dir / 'lib'
    lib_dir.mkdir(exist_ok=True)

    requirements_file = script_dir / '.github' / 'requirements.txt'
    try:
        subprocess.run(
            [
                sys.executable, '-m', 'pip', 'install',
                f'--target={lib_dir}',
                '--upgrade',
                '-q',
                '-r', str(requirements_file)
            ],
            check=True,
            cwd=script_dir
        )
        print_color("✓ Dependencies installed to lib/", GREEN)
    except subprocess.CalledProcessError:
        print_color("Error: Failed to install Python dependencies", RED)
        sys.exit(1)

    print()
    print("Generating ANTLR parser...")

    grammar_dir = script_dir / 'grammar'
    python_generated_dir = grammar_dir / 'python_generated'
    python_generated_dir.mkdir(exist_ok=True)

    # Generate Python lexer
    print("→ Generating lexer...")
    try:
        subprocess.run(
            [
                'java', '-jar', str(antlr_jar),
                '-Dlanguage=Python3',
                '-lib', '.',
                '-o', 'python_generated',
                'FeatLexerPython.g4'
            ],
            check=True,
            cwd=grammar_dir,
            capture_output=True  # Suppress ANTLR warnings
        )
    except subprocess.CalledProcessError as e:
        print_color("Error: Failed to generate lexer", RED)
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

    # Copy tokens file
    print("→ Creating token definitions...")
    tokens_src = python_generated_dir / 'FeatLexerPython.tokens'
    tokens_dst = grammar_dir / 'FeatLexer.tokens'
    shutil.copy(tokens_src, tokens_dst)

    # Generate Python parser
    print("→ Generating parser...")
    try:
        subprocess.run(
            [
                'java', '-jar', str(antlr_jar),
                '-Dlanguage=Python3',
                '-visitor',
                '-lib', '.',
                '-o', 'python_generated',
                'FeatParser.g4'
            ],
            check=True,
            cwd=grammar_dir,
            capture_output=True  # Suppress ANTLR warnings
        )
    except subprocess.CalledProcessError as e:
        print_color("Error: Failed to generate parser", RED)
        print(e.stderr.decode('utf-8'))
        sys.exit(1)

    print()
    print_color("✓ Setup complete!", GREEN)
    print()
    print("You can now validate examples:")
    print("  ./validate-examples.py                    # Validate all examples")
    print("  ./validate-examples.py path/to/file.fea   # Validate specific file")


if __name__ == '__main__':
    main()
