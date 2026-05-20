# Advanced Feature Examples

This directory contains examples of advanced OpenType feature file constructs that provide extended functionality and localization.

## Files

### Character Variant Parameters
**`cvParameters.fea`** - Complete cvParameters block example
- `FeatUILabelNameID` - Feature UI label (localized)
- `FeatUITooltipTextNameID` - Feature tooltip text (localized)
- `SampleTextNameID` - Sample text for UI (localized)
- `ParamUILabelNameID` - Parameter UI labels (localized, can be repeated)
- `Character` - Unicode values for base glyphs (decimal or hex)

Character variant features (cv01-cv99) allow font designers to provide UI strings for alternate glyph variants.

```fea
feature cv01 {
    cvParameters {
        FeatUILabelNameID {
            name 3 1 0x0409 "Alternate a";
            name 1 0 0 "Alternate a";
        };
        Character 0x61;  # Unicode for 'a'
    };
    sub a by a.alt;
} cv01;
```

### Feature Names
**`featureNames.fea`** - Multi-language feature names
**`featureNames_alternate.fea`** - Alternative featureNames usage

The `featureNames` block provides localized names for stylistic set features (ss01-ss20):

```fea
feature ss01 {
    featureNames {
        name "English description";
        name 3 1 0x411 "Japanese description";
        name 1 1 12 "Apple platform Japanese";
    };
    sub A by A.ss01;
} ss01;
```

### Size Feature Parameters
**`size_parameters.fea`** - Optical size feature parameters

The `size` feature uses a parameters statement to specify optical size information:

```fea
feature size {
    parameters 10.0 0 0 0;
} size;
```

Parameters specify: design size, subfamily ID, range minimum, range maximum.

### Anonymous Blocks
**`anonymous_block.fea`** - Anonymous block with non-standard data

Anonymous blocks allow inclusion of non-standard table data using the `anon` keyword:

```fea
anon sbit {
    /* sbit table specifications */
    72  % dpi
    sizes {
        10, 12, 14 source {
            all "Generic/JGeneric"
        }
    }
} sbit;
```

The content within anonymous blocks is not parsed by the standard grammar and is passed through to the font compiler for special handling.

## Usage Notes

- **cvParameters** must appear before any rules in the cv feature
- **featureNames** must appear before any rules in the ss feature
- **Character** values can use decimal (97) or hexadecimal (0x61) notation
- Multiple **ParamUILabelNameID** entries must match the number of variants

## Validation

```bash
# Validate an advanced feature example
../../validate-examples.py cvParameters.fea

# Validate all advanced examples
../../validate-examples.py advanced/*.fea
```
