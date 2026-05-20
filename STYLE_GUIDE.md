# Style Guide

The OpenType Feature File Specification itself is written in GitHub Markdown.
Generally speaking, changes and additions should be stylistically consistent
with analogous portions of the existing specification.

We ask, however, that authors follow the guidelines below when it comes to
section numbering.

## Specification Section Numbering Policy

**Please DO NOT renumber or modify existing section headings.** This policy ensures:
- External references remain valid (documentation, tools, blog posts)
- Automated diff tools can accurately match sections
- Clear indication of policy violations in PRs

### How to Add New Content

Use these insertion strategies to add sections **without changing existing numbers**:

#### Strategy 1: Letter Suffixes (for major insertions between sections)

**Use when**: Adding a new major subsection between existing sections

**Examples:**
```markdown
✅ GOOD: Insert between existing sections
2.e   Numbers, Locations, and Metrics (existing)
2.ea  New Major Topic (NEW - inserted)
2.eb  Another New Topic (NEW - inserted)
2.f   Glyph Classes (existing - unchanged)

9.f   OS/2 Table (existing)
9.fa  New Table Type (NEW - inserted)
9.g   vhea Table (existing - unchanged)
```

❌ **WRONG** - Do not renumber:
```markdown
❌ BAD: Renumbering existing sections
2.e   Numbers, Locations, and Metrics (existing)
2.f   New Topic (NEW)
2.g   Glyph Classes (was 2.f - RENUMBERED - breaks references!)
```

#### Strategy 2: Decimal Subdivisions (for refinements of existing sections)

**Use when**: Adding detail or variants under an existing section

**Examples:**
```markdown
✅ GOOD: Subdivide existing sections
2.e Numbers, Locations, and Metrics (existing)
  2.e.i     Integer (existing)
  2.e.ii    Float (existing)
  2.e.iii   Variable location (existing)
    2.e.iii.1  Simple variable location (NEW - subdivision)
    2.e.iii.2  Tuple-based location (NEW - subdivision)
  2.e.iv    Named location (existing - unchanged)

6.a Single Adjustment Positioning (existing)
  6.a.1  Basic positioning (NEW - subdivision)
  6.a.2  Device-specific adjustments (NEW - subdivision)
```

### Quick Reference

| Scenario | Solution | Example |
|----------|----------|---------|
| Insert between 2.e and 2.f | Use letter suffix | 2.ea, 2.eb |
| Add detail under 2.e.iii | Use decimal | 2.e.iii.1, 2.e.iii.2 |
| Insert between 9.f and 9.g | Use letter suffix | 9.fa, 9.fb |
| Add variant of existing | Use decimal | 6.a.1, 6.a.2 |

---

## Grammar Changes and Examples

### Editing the Grammar

When proposing changes to the feature file grammar:

**DO edit:**
- ✅ `grammar/FeatLexer.g4` - Token definitions, lexer rules
- ✅ `grammar/FeatParser.g4` - Parser rules, syntax structure
- ✅ Add/update files in `examples/` directory

**DO NOT edit:**
- ❌ `grammar/FeatLexerPython.g4` - Python lexer (Adobe maintains)
- ❌ `grammar/python_generated/` - Generated parser files (auto-generated)

### Including Examples

When submitting PRs that modify the grammar, please place examples of new
functionality into a new, appropriately named directory.  Example files should
be self-contained and parseable.

If changing the grammar in an incompatible way, you can edit the relevant
existing files to make your PR pass but should add comments explaining the
changes.

Example files should:
   - Be **minimal** - demonstrate just the relevant syntax
   - Be **self-contained** - parse without external dependencies where possible
   - Include **comments** explaining what's being demonstrated
   - Use **descriptive filenames** (e.g., `variable-tuple-values.fea`)
