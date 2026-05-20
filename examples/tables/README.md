# OpenType Table Examples

This directory contains examples of OpenType table definitions that control font-level metrics and behaviors.

## Files

### head Table
**`head_FontRevision.fea`** - Font header table
- `FontRevision` - Font version number

### hhea Table
**`hhea_metrics.fea`** - Horizontal header metrics
- `CaretOffset` - Caret positioning offset
- `Ascender` - Typographic ascender
- `Descender` - Typographic descender
- `LineGap` - Line spacing

### vhea Table
**`vhea_metrics.fea`** - Vertical header metrics
- `VertTypoAscender` - Vertical typographic ascender
- `VertTypoDescender` - Vertical typographic descender
- `VertTypoLineGap` - Vertical line spacing

### OS/2 Table
**`OS2_comprehensive.fea`** - Comprehensive OS/2 metrics
- `FSType` - Font embedding permissions
- `Panose` - Font classification (10 digits)
- `TypoAscender` / `TypoDescender` - Typographic metrics
- `winAscent` / `winDescent` - Windows metrics
- `UnicodeRange` - Supported Unicode ranges
- `CodePageRange` - Supported code pages
- `XHeight` / `CapHeight` - Measurement values
- `WeightClass` - Font weight (100-900)
- `WidthClass` - Font width (1-9)
- `Vendor` - Vendor ID (4 characters)
- `FamilyClass` - IBM font class

### GDEF Table
**`GDEF_LigatureCaretByIndex.fea`** - Ligature caret positioning
- `LigatureCaretByIndex` - Caret positions for ligatures by glyph index

## Usage

These table definitions typically appear at the top level of a feature file, outside of any feature blocks:

```fea
table head {
    FontRevision 1.1;
} head;

table hhea {
    Ascender 800;
    Descender -200;
    LineGap 200;
} hhea;
```

## Validation

```bash
# Validate a table example
../../validate-examples.py head_FontRevision.fea

# Validate all table examples
../../validate-examples.py tables/*.fea
```
