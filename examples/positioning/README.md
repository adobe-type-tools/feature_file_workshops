# GPOS Positioning Examples

This directory contains examples of OpenType GPOS (Glyph Positioning) rules, including advanced positioning techniques.

## Files

### Mark-to-Mark Positioning
**`mark_to_mark_contourpoint.fea`** - Mark-to-mark attachment with contour point anchors

Positions combining marks on top of other marks (e.g., stacking diacritics):

```fea
markClass [acute grave] <anchor 1 1 contourpoint 11> @TOP_MARKS;
pos mark [acute grave macron] <anchor 500 200> mark @TOP_MARKS;
```

The `contourpoint` syntax references specific points in the glyph outline for precise positioning.

### Mark-to-Base Positioning
**`mark_to_base.fea`** - Mark attachment to base glyphs

Positions combining marks relative to base character positions:

```fea
markClass [acute grave] <anchor 150 -10> @MARK;
pos base [a e o] <anchor 250 450> mark @MARK;
```

### Mark-to-Ligature Positioning
**`mark_to_ligature.fea`** - Mark attachment to ligature components

Positions marks on individual components of ligature glyphs:

```fea
pos ligature f_f_i <anchor 100 450> mark @TOP_MARKS
                    <anchor 300 450> mark @TOP_MARKS
                    <anchor 500 450> mark @TOP_MARKS ligComponent;
```

### Enumerate Positioning
**`enumerate_positioning.fea`** - Enumerate positioning syntax
**`enumerate_positioning_alt.fea`** - Alternative enumerate usage

The `enum pos` keyword creates individual pair positioning rules for all combinations:

```fea
@Y_LC = [y yacute ydieresis];
@SMALL_PUNC = [comma semicolon period];
enum pos @Y_LC @SMALL_PUNC -100;
```

This expands to individual rules:
```fea
pos y comma -100;
pos y semicolon -100;
pos y period -100;
pos yacute comma -100;
# ... etc.
```

### Cursive Attachment
**`cursive_contourpoint.fea`** - Cursive attachment with contour points

Connects glyphs in a cursive manner by aligning entry and exit points:

```fea
pos cursive @ARABIC_LETTERS <anchor 100 200 contourpoint 5>
                             <anchor 0 150 contourpoint 12>;
```

## Contour Point Anchors

Several examples use the `contourpoint` keyword to reference specific points in glyph outlines:

```fea
<anchor X Y contourpoint INDEX>
```

This allows dynamic positioning based on the actual glyph outline rather than fixed coordinates, which is useful for:
- Variable fonts where glyph shapes change
- Complex script shaping where precise attachment is critical
- Maintaining relative positions across design variations

## Validation

```bash
# Validate a positioning example
../../validate-examples.py mark_to_mark_contourpoint.fea

# Validate all positioning examples
../../validate-examples.py positioning/*.fea
```

## OpenType Specification References

- Mark positioning: OpenType spec section 6 (GPOS rules)
- Enumerate: OpenType Feature File spec section 6.b.ii
- Contour points: OpenType Feature File spec section 2.e (anchor definitions)
