# Feature File Examples

This directory contains example feature files that exercise the OpenType
Feature File grammar. These examples are primarily here to test compatibility
with grammar changes, but also serve as documentation.

The README.md files below this level are AI-generated, but may be of help
finding files that cover particular semantics.

## Directory Structure

- **basic/** - Core syntax elements (languagesystem, glyph classes, includes)
- **features/** - Feature blocks (liga, kern, mark, calt, etc.)
- **spec/** - Test files from AFDKO test suite covering specific spec sections (56 files)
- **tables/** - OpenType table definitions (head, hhea, vhea, OS/2, GDEF) (5 files)
- **advanced/** - Advanced features (cvParameters, featureNames, size, anonymous blocks) (5 files)
- **positioning/** - GPOS positioning examples (mark-to-mark, enumerate, cursive) (6 files)
- **variable/** - Variable font syntax: locationDef, variable values, axis units (6 files)
- **edge-cases/** - Corner cases, unusual but valid syntax
- **phase2/** - Work in progress features

## Adding Examples

See the (style guide)[../STYLE_GUIDE.md] for guidance on adding examples.

When submitting PRs that modify the grammar, please place examples of new
functionality into a new, appropriately named directory.  Example files should
be self-contained and parseable.

If changing the grammar in an incompatible way, you can edit the relevant
existing files to make your PR pass but should add comments explaining the
changes.

## Validation

All examples are validated automatically in CI, but can be validated locally 
with the following commands.

```bash
# Validate a single file
../validate-examples.py basic/languagesystem.fea

# Validate all examples
../validate-examples.py
```

**Note**, however, that all that is verified is that the file conforms to the
grammar alone. An actual compiler has many additional checks, e.g. to constrain
the numerical range of a value.
