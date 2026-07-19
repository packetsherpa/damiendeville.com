#!/usr/bin/env python3
"""Convert a SongShift text export into a draft Hugo daily-playlist entry."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


class SongShiftFormatError(ValueError):
    """Raised when an export cannot be parsed without guessing."""


@dataclass(frozen=True)
class Track:
    title: str
    artist: str
    album: str
    service: str
    service_id: str


@dataclass(frozen=True)
class PlaylistExport:
    exported_at: datetime
    playlist_date: date
    source_name: str
    service: str
    playlist_id: str
    tracks: tuple[Track, ...]


def _fields(line: str) -> list[str]:
    return [field.strip() for field in line.split("|")]


def parse_songshift(text: str, timezone: str = "America/New_York") -> PlaylistExport:
    lines = [(number, line.strip()) for number, line in enumerate(text.splitlines(), 1) if line.strip()]
    if not lines:
        raise SongShiftFormatError("The export is empty.")

    header_number, header_line = lines[0]
    header = _fields(header_line)
    if len(header) != 7 or header[0].lower() != "***playlist***":
        raise SongShiftFormatError(
            f"Line {header_number}: expected a seven-field SongShift playlist header."
        )

    source_name = header[1]
    if source_name.lower() != "songshift":
        raise SongShiftFormatError(
            f"Line {header_number}: expected SongShift as the export source, found {source_name!r}."
        )

    try:
        exported_at = datetime.strptime(header[2], "%m-%d-%Y %H:%M").replace(
            tzinfo=ZoneInfo(timezone)
        )
    except (ValueError, KeyError) as exc:
        raise SongShiftFormatError(
            f"Line {header_number}: invalid export timestamp {header[2]!r}."
        ) from exc

    try:
        playlist_date = datetime.strptime(header[3], "%Y.%m.%d").date()
    except ValueError as exc:
        raise SongShiftFormatError(
            f"Line {header_number}: invalid playlist date {header[3]!r}."
        ) from exc

    tracks: list[Track] = []
    identifiers: dict[tuple[str, str], int] = {}
    for line_number, line in lines[1:]:
        values = _fields(line)
        if len(values) != 5:
            raise SongShiftFormatError(
                f"Line {line_number}: expected five track fields, found {len(values)}."
            )

        title, artist, album, service, service_id = values
        if not title or not artist or not service or not service_id:
            raise SongShiftFormatError(
                f"Line {line_number}: track title, artist, service, and identifier are required."
            )

        identifier = (service.casefold(), service_id)
        if identifier in identifiers:
            raise SongShiftFormatError(
                f"Line {line_number}: duplicate track identifier also found on line "
                f"{identifiers[identifier]}."
            )
        identifiers[identifier] = line_number
        tracks.append(Track(title, artist, album, service, service_id))

    if not tracks:
        raise SongShiftFormatError("The export contains no tracks.")

    return PlaylistExport(
        exported_at=exported_at,
        playlist_date=playlist_date,
        source_name=source_name,
        service=header[5],
        playlist_id=header[6],
        tracks=tuple(tracks),
    )


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_hugo(
    playlist: PlaylistExport,
    *,
    description: str | None = None,
    playlist_url: str = "",
    threads_url: str = "",
    image: str = "",
    image_alt: str = "",
) -> str:
    display_date = (
        f"{playlist.playlist_date.strftime('%B')} "
        f"{playlist.playlist_date.day}, {playlist.playlist_date.year}"
    )
    summary = description or f"A daily playlist for {display_date}."
    exported_at = playlist.exported_at.isoformat()

    lines = [
        "---",
        f"title: {_yaml_string(f'Daily Playlist — {display_date}')}",
        f"date: {_yaml_string(playlist.playlist_date.isoformat())}",
        f"publishDate: {_yaml_string(playlist.exported_at.date().isoformat())}",
        "draft: true",
        f"description: {_yaml_string(summary)}",
        'music_kind: "Daily playlist"',
        f"playlist_url: {_yaml_string(playlist_url)}",
        f"threads_url: {_yaml_string(threads_url)}",
        f"image: {_yaml_string(image)}",
        f"image_alt: {_yaml_string(image_alt)}",
        "tags:",
        "  - playlist",
        "tracks:",
    ]

    for track in playlist.tracks:
        lines.extend(
            [
                f"  - title: {_yaml_string(track.title)}",
                f"    artist: {_yaml_string(track.artist)}",
                f"    album: {_yaml_string(track.album)}",
            ]
        )

    lines.extend(
        [
            "source:",
            f"  application: {_yaml_string(playlist.source_name)}",
            f"  exported_at: {_yaml_string(exported_at)}",
            f"  service: {_yaml_string(playlist.service)}",
            f"  playlist_id: {_yaml_string(playlist.playlist_id)}",
            "---",
            "",
            "<!-- Add a short introduction before publishing. -->",
            "",
            "<!--more-->",
            "",
            "## Why these tracks",
            "",
            "<!-- Add context before publishing. -->",
            "",
        ]
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="SongShift text export")
    parser.add_argument("--output", type=Path, help="Write the draft to this Markdown file")
    parser.add_argument("--description", help="One-sentence playlist description")
    parser.add_argument("--playlist-url", default="", help="Public playlist URL")
    parser.add_argument("--threads-url", default="", help="Related Threads post URL")
    parser.add_argument("--image", default="", help="Public image path")
    parser.add_argument("--image-alt", default="", help="Image description")
    parser.add_argument("--timezone", default="America/New_York", help="Export timestamp timezone")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        playlist = parse_songshift(args.export.read_text(encoding="utf-8-sig"), args.timezone)
        output = render_hugo(
            playlist,
            description=args.description,
            playlist_url=args.playlist_url,
            threads_url=args.threads_url,
            image=args.image,
            image_alt=args.image_alt,
        )
    except (OSError, SongShiftFormatError) as exc:
        raise SystemExit(f"error: {exc}") from exc

    if args.output:
        if args.output.exists() and not args.force:
            raise SystemExit(f"error: {args.output} already exists; use --force to replace it")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(args.output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
