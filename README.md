# cropdf

**cropdf** automatically removes unnecessary whitespace from PDF figures, making them easier to fit into LaTeX documents.

Simply run:

```bash
cropdf figure.pdf
```

## Features

* Automatically crop PDF pages to their visible content while preserving original PDF quality.
* Process multiple files at once.
* Support wildcard patterns and recursive searches.


## Installation

```bash
git clone https://github.com/trongdx2003/cropdf.git
cd cropdf
pip install .
```

For development:

```bash
pip install -e .
```

## Usage

Crop a single PDF:

```bash
cropdf figure.pdf
```

This creates:

```text
figure-cropped.pdf
```

### Multiple files

```bash
cropdf file1.pdf file2.pdf file3.pdf
```

### Wildcard patterns

```bash
cropdf *.pdf
```

### Recursive globbing

```bash
cropdf "**/*.pdf" -r
```

### Output directory

```bash
cropdf *.pdf -o cropped
```

### Parallel processing

```bash
cropdf *.pdf -w 8
```

## Command-Line Options

| Option                   | Description                      |
|--------------------------| -------------------------------- |
| `-o`, `--outdir DIRNAME` | Output directory                 |
| `-r`, `--recursive`      | Enable recursive globbing (`**`) |
| `-w`, `--workers N`      | Number of parallel workers       |

## Examples

Crop all PDFs in the current directory:

```bash
cropdf *.pdf
```

Crop all PDFs recursively and save results to another directory:

```bash
cropdf "**/*.pdf" -r -o cropped
```

## Requirements

* Python 3.10+
* PyMuPDF
* NumPy
