# Specification Test Files

This directory contains 56 feature files from AFDKO's test suite that exercise specific sections of the OpenType Feature File Specification. Each file tests grammar elements defined in particular spec sections.

## File Naming Convention

Files are named `{section}-{test_number}.fea` where:
- `{section}` corresponds to the spec section (e.g., `4bi` = section 4.b.i)
- `{test_number}` distinguishes multiple tests for the same section

**Example:** `4bi-2.fea` is test #2 for section 4.b.i (languagesystem)

## Coverage by Specification Section

### Section 2: Syntax

**2.e.vii - Named value record** (3 tests)
- `2evii-1.fea` - valueRecordDef with Format A
- `2evii-4.fea` - valueRecordDef usage

**2.e.x - Named anchor definition** (1 test)
- `2ex-1.fea` - anchorDef keyword

**2.g.i - Glyph class ranges** (2 tests)
- `2gi-1.fea` - Basic glyph classes
- `2gi-6.fea` - Glyph class with CID ranges

**2.g.ii - Named glyph classes** (1 test)
- `2gii-1.fea` - Named glyph class definitions

### Section 3: Including Files

**3 - include statement** (1 test)
- `3-2.fea` - File inclusion

### Section 4: Specifying Features

**4.b.i - languagesystem** (4 tests)
- `4bi-2.fea` - Wrong dflt script and DFLT language
- `4bi-3.fea` - languagesystem declarations
- `4bi-4.fea` - Multiple language systems
- `4bi-5.fea` - languagesystem with script variations

**4.b.ii - script and language** (1 test)
- `4bii-1.fea` - Deprecated includeDFLT and excludeDFLT

**4.d - lookupflag** (3 tests)
- `4d-2.fea` - lookupflag usage
- `4d-8.fea` - lookupflag with marks
- `4d-10.fea` - lookupflag combinations

**4.e - lookup** (2 tests)
- `4e-12.fea` - Lookup block definitions
- `4e-13.fea` - Lookup references

**4.g - subtable** (3 tests)
- `4g-3.fea` - Subtable breaks
- `4g-4.fea` - Subtable organization
- `4g-5.fea` - Subtable in lookup

### Section 5: Glyph Substitution (GSUB) Rules

**5.b - Multiple substitution** (1 test)
- `5b-1.fea` - Multiple substitution rule

**5.f.ii - Chaining contextual exceptions** (3 tests)
- `5fii-1.fea` - Deprecated except statement
- `5fii-2.fea` - Exception handling
- `5fii-3.fea` - Contextual exceptions

**5.h - Reverse chaining substitution** (1 test)
- `5h-2.fea` - Reverse chaining single substitution

### Section 6: Glyph Positioning (GPOS) Rules

**6.d - Mark-to-Base attachment** (1 test)
- `6d-3.fea` - Mark-to-base positioning

**6.h.vi - Contextual positioning exceptions** (2 tests)
- `6hvi-1.fea` - Chain positioning exceptions
- `6hvi-3.fea` - Contextual positioning rules

### Section 8: Specially Handled Features

**8.a - aalt feature** (7 tests)
- `8a-2.fea` - All alternates feature
- `8a-4.fea` - aalt with multiple features
- `8a-5.fea` - aalt feature combinations
- `8a-6.fea` - aalt with lookups
- `8a-7.fea` - Complex aalt structures
- `8a-9.fea` - aalt feature variations
- `8a-11.fea` - aalt with contextual rules

### Section 9: Specifying Table Values

**9.a - BASE table** (2 tests)
- `9a-1.fea` - BASE table definitions
- `9a-4.fea` - BASE table with multiple scripts

**9.b - GDEF table** (2 tests)
- `9b-3.fea` - GDEF GlyphClassDef
- `9b-4.fea` - GDEF table structure

**9.e - name table** (1 test)
- `9e-14.fea` - name table entries

**9.f - OS/2 table** (5 tests)
- `9f-3.fea` - OS/2 UnicodeRange
- `9f-6.fea` - OS/2 table values
- `9f-7.fea` - OS/2 attributes
- `9f-9.fea` - OS/2 version
- `9f-10.fea` - OS/2 extended values

**9.h - vmtx table** (1 test)
- `9h-1.fea` - vmtx vertical metrics

**9.i - STAT table** (10 tests)
- `9i-1.fea` - STAT table with AxisValue formats
- `9i-2.fea` - STAT DesignAxis
- `9i-3.fea` - STAT with multiple axes
- `9i-4.fea` - STAT AxisValue variations
- `9i-5.fea` - STAT ElidedFallbackName
- `9i-6.fea` - STAT flags
- `9i-20.fea` - STAT format 1
- `9i-21.fea` - STAT format 2
- `9i-22.fea` - STAT format 3
- `9i-25.fea` - STAT format 4

## Validation

All files in this directory must parse successfully with the grammar:

```bash
# Validate a single file
../../validate-examples.py 4bi-2.fea

# Validate all spec examples
../../validate-examples.py spec/*.fea
```

## Notes

- These files are derived from AFDKO's test suite and represent real-world grammar usage
- File names were updated to reflect current spec section numbers (variable features additions in 2024 shifted section 2.e numbering)
- Original test names: `2ev-*.fea` renamed to `2evii-*.fea`, `2eviii-1.fea` renamed to `2ex-1.fea`
- Not all spec sections are represented - these tests focus on areas with the most historical test coverage
