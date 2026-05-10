# Report Folder

Place the LaTeX source files and the compiled PDF for the final report here at submission time.

## Expected files at submission

- `task2report.tex` - the populated IEEEtran template.
- `references.bib` - the BibTeX bibliography.
- `task2report.pdf` - the compiled report.
- `figs/` - any figures referenced by the report.

## Source of truth during development

I drafted the report in Overleaf to take advantage of its real IEEEtran installation and live preview. Before submission I will:

1. Download the project as a zip from Overleaf (Menu -> Source -> Download).
2. Copy `task2report.tex`, `references.bib`, the compiled `task2report.pdf`, and the `figs/` folder into this directory.
3. Commit and push.

## Bibliography requirement

Per the lecturer's brief, every reference must include a working clickable link. The `.bib` file uses the IEEEtran-friendly `url={...}` field on every entry, which IEEEtran.bst renders as a clickable DOI/URL line in the bibliography.

Before submission I will click through every URL in the bib file in a private browsing window to confirm each resolves.

## How to compile (once files are committed)

```bash
cd report
pdflatex task2report
bibtex task2report
pdflatex task2report
pdflatex task2report
```

The four-pass sequence is needed for cross-references (figures, tables, sections) and for the bibliography numbering.

## Declaration of Originality

The IEEEtran template includes a Declaration of Originality block on the first page. The GenAI disclosure paragraph in that block is filled out to declare the limited supporting role of Claude (Anthropic) for language refinement, while affirming that all intellectual content is my own.
