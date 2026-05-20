# Contributing

Thank you for your interest in the OpenType Feature File Specification Workshops.

This is a specification repository, not a software project, so contributions take
a different form than in a typical open-source codebase. The primary paths are
described in detail in the [README](README.md); this document summarizes what
to know before submitting.

## Submitting a proposal (PR)

A proposal is a pull request that changes the specification. To be considered,
a proposal should include:

1. An explanation in the PR summary of the purpose of the change and its expected
   implementation in feature file compilers
2. Edits to [OpenTypeFeatureFileSpecification.md](OpenTypeFeatureFileSpecification.md)
3. Edits to the ANTLR4 grammar files in [grammar/](grammar/) covering the proposed
   syntax changes
4. Example `.fea` files in [examples/](examples/) illustrating the new grammar,
   with comments

Please follow the [Style Guide](STYLE_GUIDE.md) for all edits to the specification,
particularly the section-numbering policy.

See [TOOLS.md](TOOLS.md) for instructions on generating a local HTML preview of
your changes and validating example files against the grammar before submitting.

## Submitting an idea (issue)

If you have a suggestion but are not ready to write a full proposal, open an issue.
See the README for guidance on what makes a useful idea submission.

## Participating in discussions

GitHub Discussions is available for topics that do not fit neatly into a PR or issue.

## Intellectual property

The specification is licensed under the Apache License 2.0. By contributing, you
agree that your contribution may be incorporated under that license. Contributions
involving patented technology or incompatible intellectual property rights are out
of scope.

## Code of Conduct

All participants are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
