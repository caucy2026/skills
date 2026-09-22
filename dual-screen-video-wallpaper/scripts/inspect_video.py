#!/usr/bin/env python3
"""Validate a wallpaper video with ffmpeg and emit a JSON report."""

import argparse
import json
import re
import subprocess
from pathlib import Path


def run(args):
    return subprocess.run(args, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--fps", type=float, default=30.0)
    parser.add_argument("--fps-tolerance", type=float, default=0.02)
    parser.add_argument("--black-duration", type=float, default=0.01)
    parser.add_argument("--black-threshold", type=float, default=0.10)
    args = parser.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"missing video: {args.video}")

    probe = run([args.ffmpeg, "-hide_banner", "-i", str(args.video)])
    text = probe.stderr
    video = re.search(
        r"Video:\s*([^,]+).*?(\d+)x(\d+).*?(\d+(?:\.\d+)?) fps", text
    )
    duration = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
    if not video or not duration:
        raise SystemExit("could not parse ffmpeg stream metadata")

    codec = video.group(1).strip()
    width, height, fps = int(video.group(2)), int(video.group(3)), float(video.group(4))
    seconds = int(duration.group(1)) * 3600 + int(duration.group(2)) * 60 + float(duration.group(3))
    audio = len(re.findall(r"Stream #.*Audio:", text))

    decoded = run([
        args.ffmpeg, "-v", "error", "-i", str(args.video), "-an", "-f", "null", "-"
    ])
    black = run([
        args.ffmpeg, "-hide_banner", "-i", str(args.video), "-vf",
        f"blackdetect=d={args.black_duration}:pix_th={args.black_threshold}",
        "-an", "-f", "null", "-"
    ])
    intervals = [line.strip() for line in black.stderr.splitlines() if "black_start:" in line]

    report = {
        "path": str(args.video.resolve()),
        "codec": codec,
        "width": width,
        "height": height,
        "fps": fps,
        "duration_seconds": seconds,
        "audio_streams": audio,
        "black_intervals": intervals,
        "full_decode_passed": decoded.returncode == 0,
        "decode_errors": decoded.stderr.strip(),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    failures = []
    if (width, height) != (args.width, args.height):
        failures.append(f"size is {width}x{height}")
    if abs(fps - args.fps) > args.fps_tolerance:
        failures.append(f"fps is {fps}")
    if audio:
        failures.append(f"contains {audio} audio stream(s)")
    if intervals:
        failures.append("contains black interval(s)")
    if decoded.returncode:
        failures.append("full decode failed")
    if failures:
        raise SystemExit("; ".join(failures))


if __name__ == "__main__":
    main()
