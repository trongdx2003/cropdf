from __future__ import annotations

import argparse
import sys

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

from .crop import expand_patterns, process_file


def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument("files", nargs="+", help="Input PDF files or patterns")
    parser.add_argument("-o", "--outdir", help="Output directory")
    parser.add_argument("-r", "--recursive", action="store_true", help="Enable recursive globbing")
    parser.add_argument("-w", "--workers", type=int, default=8, help="Number of parallel workers")

    args = parser.parse_args(argv)

    outdir = Path(args.outdir) if args.outdir else None

    if outdir:
        outdir.mkdir(parents=True, exist_ok=True)

    expanded_files = expand_patterns(args.files, recursive=args.recursive)

    if not expanded_files:
        print("No files to process.", file=sys.stderr)
        return

    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=min(args.workers, len(expanded_files))) as executor:
            futures = [
                executor.submit(process_file, file, outdir) for file in expanded_files
            ]

            for future in as_completed(futures):
                print(future.result())
    else:
        for file in expanded_files:
            print(process_file(file, outdir))


if __name__ == "__main__":
    main()