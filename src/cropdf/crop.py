from __future__ import annotations

import sys
import glob
import fitz
import numpy as np

from pathlib import Path


def detect_bbox(page: fitz.Page, zoom: float = 2.0, white_thresh: int = 250):
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)

    n = pix.n
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    arr = arr.reshape((pix.h, pix.w, n))

    if n >= 3:
        mask = (arr[:, :, :3].min(axis=2) < white_thresh)
    else:
        mask = (arr < white_thresh)

    coords = np.argwhere(mask)
    if coords.size == 0:
        return None

    ys, xs = coords[:, 0], coords[:, 1]

    x0_px, x1_px = xs.min(), xs.max()
    y0_px, y1_px = ys.min(), ys.max()

    x0 = x0_px / zoom
    y0 = y0_px / zoom
    x1 = (x1_px + 1) / zoom
    y1 = (y1_px + 1) / zoom

    return fitz.Rect(x0, y0, x1, y1)


def auto_crop_page(page: fitz.Page):
    bbox = detect_bbox(page)

    if bbox is None:
        return

    bbox = bbox & page.rect
    if bbox.is_empty:
        return

    page.set_cropbox(bbox)


def crop_pdf(input_path: Path, output_path: Path):
    doc = fitz.open(str(input_path))

    for page in doc:
        auto_crop_page(page)

    doc.save(str(output_path))
    doc.close()


def expand_patterns(patterns, recursive=False):
    files = []

    for pattern in patterns:
        matches = glob.glob(pattern, recursive=recursive)

        if not matches:
            print(f"No matches found for pattern: {pattern}", file=sys.stderr)

        files.extend(matches)

    return list(dict.fromkeys(files))


def process_file(file, outdir):
    in_path = Path(file)

    if not in_path.exists():
        return f"File not found: {in_path}"

    if in_path.suffix.lower() != ".pdf":
        return f"Skipping non-PDF: {in_path}"

    if outdir:
        out_path = outdir / (in_path.stem + "-cropped.pdf")
    else:
        out_path = in_path.with_name(in_path.stem + "-cropped.pdf")

    try:
        crop_pdf(in_path, out_path)
        return f"Saved: {out_path}"
    except Exception as e:
        return f"Error processing {in_path}: {e}"