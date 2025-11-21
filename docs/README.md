# Documentation Compilation Guide
## Prerequisites

You need a LaTeX distribution installed on your system:

- **Linux/WSL**: `sudo apt-get install texlive-latex-base texlive-latex-extra texlive-bibtex-extra`

## Compilation Instructions

### Full Compilation (with Bibliography)

```bash
cd docs
pdflatex literature_review.tex
bibtex literature_review
pdflatex literature_review.tex
pdflatex literature_review.tex
```

**Why multiple runs?**
1. **First `pdflatex`** - Processes the document and creates `.aux` file with citation information
2. **`bibtex`** - Reads the `.aux` file, processes `references.bib`, and generates `.bbl` file
3. **Second `pdflatex`** - Incorporates the bibliography from `.bbl` file
4. **Third `pdflatex`** - Resolves all cross-references and ensures everything is up to date

### Quick Compilation (content changes only)

If you've only edited the text content without changing citations:

```bash
pdflatex literature_review.tex
```

### Using Make (Optional)

For convenience, you can create a simple Makefile or use this one-liner:

```bash
pdflatex literature_review.tex && bibtex literature_review && pdflatex literature_review.tex && pdflatex literature_review.tex
```

## Output Files

After compilation, these files will be generated:

- `literature_review.pdf` - Final PDF document
- `literature_review.aux` - Auxiliary file with cross-reference information
- `literature_review.bbl` - Formatted bibliography
- `literature_review.blg` - BibTeX log file
- `literature_review.log` - LaTeX compilation log
- `literature_review.out` - Hyperref outline data

## IDE/Editor Options

### VSCode with LaTeX Workshop

1. Install the "LaTeX Workshop" extension
2. Open `literature_review.tex`
3. Press `Ctrl+Alt+B` (or `Cmd+Option+B` on macOS) to build
4. The extension will automatically run the full compilation cycle

### TeXstudio

1. Open `literature_review.tex`
2. Go to Tools → Commands → BibTeX
3. Then Tools → Build & View (or press F5)

### Overleaf

1. Upload `literature_review.tex` and `references.bib` to a new project
2. Compilation is automatic - just edit and save

## Troubleshooting

### Bibliography not showing?

- Make sure you've run the full 4-step compilation cycle
- Check that `references.bib` is in the same directory as the `.tex` file
- Look for errors in the `.blg` file: `cat literature_review.blg`

### Citation warnings?

If you see "Citation ... undefined" warnings:
- Run the compilation cycle one more time
- Make sure the citation keys in `\cite{}` match entries in `references.bib`

### Missing packages?

If you get "File not found" errors for packages:
- **Ubuntu/Debian**: `sudo apt-get install texlive-full`
- **MiKTeX**: Packages install automatically on first use (if enabled)

### Clean build

To remove all generated files and start fresh:

```bash
rm literature_review.{aux,bbl,blg,log,out,pdf}
```

Then run the full compilation cycle again.

## Adding New References

1. Add entries to `references.bib` in BibTeX format
2. Cite them in the `.tex` file using `\cite{citation-key}`
3. Run the full compilation cycle to update the bibliography

## Formatting LaTeX Files

To automatically format and clean up your `.tex` files, use `latexindent` (also known as `fmt-tex`):

### Installation

- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install latexindent
  ```
- **macOS** (with Homebrew):
  ```bash
  brew install latexindent
  ```
- **Included with**: TeX Live 2018+ and MiKTeX

### Format a file in-place

```bash
latexindent -w literature_review.tex
```

The `-w` flag writes the formatted output back to the original file. A backup will be created as `literature_review.bak0`.

### Preview formatting without modifying

```bash
latexindent literature_review.tex
```

This prints the formatted output to the terminal without modifying the file.

### Format without creating backup

```bash
latexindent -w -c=/tmp literature_review.tex
```

The `-c=/tmp` flag puts the backup in `/tmp` instead of cluttering your working directory.

### Format all .tex files

```bash
for file in *.tex; do latexindent -w "$file"; done
```

### VSCode Integration

If you use VSCode with LaTeX Workshop:
1. Install the extension
2. Right-click in a `.tex` file
3. Select "Format Document" or press `Shift+Alt+F` (Windows/Linux) or `Shift+Option+F` (macOS)

### Configuration

You can customize formatting rules by creating a `.latexindent.yaml` file in your home directory or project root. See the [latexindent documentation](https://latexindentpl.readthedocs.io/) for options.

## Document Format

- **Document class**: article (12pt)
- **Margins**: 1 inch on all sides
- **Spacing**: Double-spaced
- **Bibliography style**: IEEEtran
