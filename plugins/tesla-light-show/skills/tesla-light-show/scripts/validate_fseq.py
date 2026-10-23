#!/usr/bin/env python3
"""
Non-interactive .fseq validator for Tesla light shows.

Applies the same checks as Tesla's official validator
(https://github.com/teslamotors/light-show/blob/master/validator.py):
  - magic "PSEQ", data offset >= 24, frame count >= 1, step time >= 15 ms
  - channel count is exactly 48 or 200
  - compression type 0 (uncompressed)
  - total duration <= 4 hours
  - warns if version is not 2.0 / 2.2

Unlike the official script it never prompts for input, and the exit code
reflects the result: 0 = valid, 1 = invalid, 2 = usage / IO error.

Usage: python3 validate_fseq.py show.fseq [more.fseq ...]
"""
import datetime
import struct
import sys


class ValidationError(Exception):
    pass


def validate(path):
    with open(path, "rb") as f:
        header = f.read(21)
    if len(header) < 21:
        raise ValidationError("Unknown file format, expected FSEQ v2.0")
    magic = header[0:4]
    start, minor, major = struct.unpack("<HBB", header[4:8])
    channel_count, frame_count, step_time = struct.unpack("<IIB", header[10:19])
    compression_type = header[20]

    if magic != b"PSEQ" or start < 24 or frame_count < 1 or step_time < 15:
        raise ValidationError("Unknown file format, expected FSEQ v2.0")
    if channel_count not in (48, 200):
        raise ValidationError(f"Expected 48 or 200 channels, got {channel_count}")
    if compression_type != 0:
        raise ValidationError("Expected file format to be V2 Uncompressed")
    duration_s = frame_count * step_time / 1000
    if duration_s > 4 * 60 * 60:
        raise ValidationError(
            "Expected total duration to be less than 4 hours, got "
            f"{datetime.timedelta(seconds=duration_s)}"
        )
    warning = None
    if minor not in (0, 2) or major != 2:
        warning = (f"WARNING: FSEQ version is {major}.{minor}. "
                   "Only version 2.0 and 2.2 have been validated.")
    return channel_count, frame_count, step_time, duration_s, warning


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    rc = 0
    for path in argv[1:]:
        try:
            ch, frames, step, dur, warning = validate(path)
        except OSError as e:
            print(f"{path}: ERROR {e}")
            rc = max(rc, 2)
            continue
        except ValidationError as e:
            print(f"{path}: INVALID {e}")
            rc = max(rc, 1)
            continue
        print(f"{path}: OK Found {frames} frames, step time of {step} ms for a "
              f"total duration of {datetime.timedelta(seconds=dur)} ({ch} channels).")
        if warning:
            print(f"{path}: {warning}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
