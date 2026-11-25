#!/usr/bin/env python3
"""make.fun news-image-20261124 entry.

Writes the pre-made front-page image (entry.png, in this repository) to
/output/entry.png. Pure file copy: no network, no randomness, no clock,
so two runs produce byte-identical output. The bundled image is validated
before copying, the output is validated again after copying, and a short
summary is printed.
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"
MAX_BYTES = 1024 * 1024
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path):
    """Return (width, height) of a PNG file, or None if not a valid PNG."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        return None
    # First chunk must be IHDR: length (4) + type (4) + data (13).
    length, ctype = struct.unpack(">I4s", header[8:16])
    if ctype != b"IHDR" or length != 13:
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_image(path, label):
    """Check a PNG file against the competition limits.

    Returns a list of failure messages; an empty list means the file is fine.
    All checks run, so one report lists every problem instead of only the
    first one found.
    """
    try:
        size = os.path.getsize(path)
    except OSError as exc:
        return ["%s: cannot read file (%s)" % (label, exc)]
    failures = []
    dims = png_dimensions(path)
    if dims is None:
        failures.append("%s: not a valid PNG" % label)
    elif dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        failures.append(
            "%s: dimensions %dx%d, expected %dx%d"
            % (label, dims[0], dims[1], EXPECTED_WIDTH, EXPECTED_HEIGHT)
        )
    if size > MAX_BYTES:
        failures.append("%s: %d bytes, over the 1 MiB limit" % (label, size))
    return failures


def main():
    # Fail fast if the bundled image itself does not meet the limits.
    failures = validate_image(SRC, "entry.png")
    if failures:
        raise SystemExit("validation failed:\n  " + "\n  ".join(failures))

    out_dir = os.path.dirname(DST)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, DST)
    os.chmod(DST, 0o644)

    failures = validate_image(DST, "output")
    if failures:
        raise SystemExit("validation failed:\n  " + "\n  ".join(failures))
    size = os.path.getsize(DST)
    dims = png_dimensions(DST)
    digest = sha256_of(DST)
    print(
        "wrote %s: %dx%d, %d bytes, sha256 %s"
        % (DST, dims[0], dims[1], size, digest)
    )


if __name__ == "__main__":
    main()
