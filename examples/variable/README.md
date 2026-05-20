# Variable Font Syntax Examples

This directory contains examples of the variable font syntax extensions to the OpenType Feature File Specification.

## Overview

These examples demonstrate the grammar extensions that support variable fonts:
- **locationDef** statements for defining axis locations
- **Variable value syntax** for location-specific values with min/default/max
- **Inline location specifiers** with the `(axis=value:number)` syntax
- **Axis unit designators** (`d`, `u`, `n`)

## Key Requirements

### Variable Values Must Specify Min, Default, and Max

All variable values must define three control points for each axis:

```fea
# Correct: min, default, max for wght axis
valueRecordDef (50 wght=200d:-30 wght=900d:-60) KERN_A_a;
anchorDef (300 wght=200d:280 wght=900d:320) 550 top;

# Pattern: (default_value min_location:min_value max_location:max_value)
```

### Never Define locationDef at the Default Point

Do not create named locations for the default axis values (e.g., wght=400d), as they are redundant:

```fea
# Correct - only non-default locations
locationDef wght=200d @ExtraLight;
locationDef wght=900d @Black;

# Incorrect - avoid default point
# locationDef wght=400d @Regular;  ❌
```

### Inline Location Syntax Works Without Spaces

Inline location specifiers now work **without requiring spaces**:

```fea
# This works! (previously required spaces around the colon)
valueRecordDef (50 wght=200d:-30 wght=900d:-60) KERN;
anchorDef (250 wght=200d:240 wght=900d:260) 620 top;
```

## Example Files

### Foundation Examples
- **locationDef_basic.fea** - Basic location definition syntax
- **axis_unit_d_as_glyph.fea** - Tests that 'd' works as a glyph name
- **axis_unit_u_as_glyph.fea** - Tests that 'u' works as a glyph name
- **axis_unit_n_as_glyph.fea** - Tests that 'n' works as a glyph name

### Key Tests
- **whitespace_inline.fea** - The key test: inline locations work without spaces
- **variable_comprehensive.fea** - Comprehensive test of all variable font features

## Grammar Features

### locationDef Statement
Define named locations in the design space:
```fea
locationDef wght=400d @Regular;
locationDef wght=400d, opsz=12d @RegularSmall;
```

### Variable Values
Values that vary across the design space (must include min, default, and max):
```fea
# Simple variable value (single number)
valueRecordDef (50 wght=200d:-30 wght=900d:-60) KERN_A_a;

# Variable value record (four-value positioning)
valueRecordDef (<0 0 -40 0> wght=200d:<0 0 -30 0> wght=900d:<0 0 -60 0>) KERN_A_b;

# Variable anchors
anchorDef (300 wght=200d:280 wght=900d:320) 550 top;

# Using named locations
valueRecordDef (50 @ExtraLight:-30 @Black:-60) KERN_NAMED;
```

### Axis Unit Designators
- `d` - Design units (as defined in designspace file)
- `u` - User units (as exposed to users)
- `n` - Normalized units (-1.0 to 1.0)

## Technical Details

These examples require the lexer modes implementation that:
1. Removes AXISUNIT tokens from the default lexer mode
2. Adds LocationDefMode for `locationDef` statements
3. Adds VarValue mode for inline location specifiers in parentheses

This eliminates the tokenization ambiguity that previously prevented `d:47` from parsing correctly as AXISUNIT + COLON + NUM in inline locations.

## Source

These examples are derived from the test suite in afdko5, specifically from `tests/addfeatures_data/input/var/`. All files have been fixed to include proper min/default/max values for variable value syntax and tested with addfeatures to ensure they build successfully.
