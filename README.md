# OpenType Feature File Specification Workshops

## Overview

Adobe will host a series of technical meetings about the OpenType Feature File
Specification in order to to:

- Enable collaborative discussion absent a formal standards body
- Help move the specification forward
- Reduce fragmentation across implementations

This repository provides a forum for gathering proposals (in the form of PRs to
change the specification and feature file grammar) and ideas (in the form of issues)
prior to the technical meetings. Although most of the participants in the meetings
themselves will be developers of the tools that implement the specification, proposals
and ideas from a wider audience are welcome. Keep in mind, though, that proposals
along these lines are most likely to be of interest to the reviewers:

- Catching up with syntax changes implemented or proposed in non-AFDKO compilers,
  and therefore not yet included in the current specification
- Support for variable fonts
- Smaller proposals that will easily fit into the existing system

Adobe has proposed additions to support variable values in feature files that
are already included in this draft specification, and will be proposing changes
to support feature variations (e.g. axis-controlled substitution). Both will be
discussed as part of this process.

## Current project phase: Submission and early discussion

We are currently in the first phase of the process when proposals and ideas are
being collected. The eventual schedule of meetings is still to be determined,
and will depend in part on what is submitted and ongoing communication among
potential reviewers. However, we ask that anyone who may wish to submit something
either add an issue or PR or contact us at
<feature-file-workshops@adobe.com> by the deadline below.

> [!IMPORTANT]
> The deadline for initial proposals and participation requests is **August 15th, 2026**.

## Initial status of specification

The version of the specification we are starting with was the one reviewed last
year in
[adobe-type-tools/feature_file_change_review](https://github.com/adobe-type-tools/feature_file_change_review)
The most significant change was adding support for variable values in feature
files, but the grammar has also been updated to add a number of OS/2 and hhea
fields that were simply absent from the AFDKO grammar: the subscript and
superscript size and offset fields, `StrikeoutSize`, `StrikeoutPosition`,
`CaretSlopeRise`, and `CaretSlopeRun`.

Our starting from that point does reflect our belief that those changes are 
well motivated and structured. However, this should not be seen as our taking
further changes "off the table". We recognize that these parts of the grammar
can be modified more easily than other parts given how recently they were
introduced.

## How to participate

### Submit a proposal as a PR

Anyone can make a proposal to add to or change the feature file specification
by submitting a PR to this repository. It is strongly preferred that proposals
include the following, and that all changes follow the [style
guide](STYLE_GUIDE.md):

1. An explanation, in the PR summary, of the purpose of the changes and the
   expected implementation in feature file compilers.
2. Edits to the specification itself
3. Edits to the Antlr4 tokenizer and parser files encompassing the proposed
changes to the feature file grammar.
4. Example feature files making use of the grammar, with comments.

Changes to the variable feature guide, when relevant, are also appreciated.

Submitters should be prepared to respond to questions about their proposals
and to make changes if requested.

### Submit an idea as an issue

If you have an idea for how the feature file specification might be changed,
or want to raise a concern about something the current specification does not
support or only supports in a limited or inconvenient way, and are not able
to develop the idea into a full proposal, you can communicate the idea by
opening an issue in this respository.

There are no particular guidelines for issues beyond the usual plea not to
waste other participants' time. For any idea to have an effect on the
specification it will need to be developed into a proposal in some form,
presumably by some other participant. Focused ideas about clear needs are
the most likely to garner the right kind of interest.

### Participate in the technical meetings

Much of the value of the OpenType Feature File Specification comes from it
being supported in multiple font tools stacks and contexts, so that font
developers can switch between different tools with minimal effort. This value
rests on the common interest of the developers of such tools—functionality
added to the specification but not implemented in compilers is of little
benefit. Accordingly, we hope that the *primary* participants in the technical
meetings will be developers of tools that implement the feature file grammar.

If you are a tool developer who would like to participate please contact us at
<feature-file-workshops@adobe.com> telling us a bit about the tool, the extent
you think you will be able to participate, and the github usernames of
potential attendees. We will work with you to arrive at a schedule in the later
stages of this process, and may also direct you to specific issues, PRs, or
discussions in this repository. We expect to create a *schedule* issue later in
the process that participants can watch to get updates and comment on to raise
concerns.

In addition to tool developers, we think it would be valuable to have some
experienced font engineers participate in the meetings. If you are a
sophisticated user of feature files in font development, or are knowledgable
about an area in which there is a significant proposal, please also reach
out to us at <feature-file-workshops@adobe.com>

### Start a discussion

If you have some concern that does not fall neatly into any of these categories,
and have reviewed the other sections of this repository for potential answers,
you can also create a new discussion. 

### Intellectual property note

Please remember that the specification itself is available under the Apache
License, and any additions or changes to the copy Adobe maintains will continue
to available under this license. Accordingly, inclusion of patented technology
or other features with incompatible intellectual property rights is out of
scope of these workshops.

## The font tools community

In some initial discussion about these workshops, other developers of font
tools expressed interest in better communication across the community. While
that need is mostly beyond the scope of this repository, we are hosting 
a discussion on the subject.

## File Structure

- **[OpenTypeFeatureFileSpecification.md](OpenTypeFeatureFileSpecification.md)** — Current specification (baseline)
- **grammar/** — Antlr4 grammar files from AFDKO
- **examples/** — Example feature files
- **[Variable_Feature_Guide.md](Variable_Feature_Guide.md)** — Guide to variable feature file syntax
- **[STYLE_GUIDE.md](STYLE_GUIDE.md)** — Guidelines for PRs
- **[TOOLS.md](TOOLS.md)** — Notes on the specification preview and grammar checking tools in this repository
- **LICENSE.md** — Apache License 2.0

## Contact

If you have questions not answered here you can contact <feature-file-workshops@adobe.com>

## License

Copyright 2025 Adobe. Licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE) file for details.
