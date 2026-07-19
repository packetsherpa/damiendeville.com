#!/usr/bin/env python3
"""Backfill Hugo daily playlist pages from dated SongShift exports."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.songshift_to_hugo import parse_songshift
from scripts.sync_daily_playlists import backfill_playlist_url, render_published_entry


DATE_EXPORT_RE = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})\.txt$")
REVIEW_PATH = Path("PLAYLIST_HEADER_REVIEW.md")


@dataclass(frozen=True)
class ParsedExport:
    path: Path
    filename_date: str
    playlist_date: str
    exported_at: str
    content: object


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("~/Documents/playlists").expanduser(),
        help="Directory containing dated SongShift exports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("content/music/daily"),
        help="Directory where Hugo daily playlist pages live.",
    )
    parser.add_argument(
        "--review-path",
        type=Path,
        default=REVIEW_PATH,
        help="Markdown file to write with issues that need later review.",
    )
    parser.add_argument(
        "--timezone",
        default="America/New_York",
        help="Timezone used when parsing SongShift exports.",
    )
    parser.add_argument(
        "--today",
        default=date.today().isoformat(),
        help="Treat playlist dates after this YYYY-MM-DD value as future-dated.",
    )
    return parser


def iter_dated_exports(source_dir: Path) -> list[tuple[Path, str]]:
    exports: list[tuple[Path, str]] = []
    for path in sorted(source_dir.iterdir()):
        if not path.is_file():
            continue
        match = DATE_EXPORT_RE.match(path.name)
        if not match:
            continue
        filename_date = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        exports.append((path, filename_date))
    return exports


def pick_canonical(exports: list[ParsedExport]) -> ParsedExport:
    return max(
        exports,
        key=lambda item: (
            item.filename_date == item.playlist_date,
            item.exported_at,
            item.path.name,
        ),
    )


def write_review(
    path: Path,
    *,
    today: str,
    total_exports: int,
    generated: int,
    existing: int,
    backfilled: int,
    parse_errors: list[tuple[str, str]],
    mismatches: list[tuple[str, str, str]],
    duplicates: list[tuple[str, list[ParsedExport], ParsedExport]],
    future_dated: list[ParsedExport],
) -> None:
    lines = [
        "# Playlist Header Review",
        "",
        "This report was generated during the dated-playlist backfill sweep so that questionable exports could be reviewed later without halting page generation.",
        "",
        "## Summary",
        "",
        f"- Sweep date basis: `{today}`",
        f"- Dated exports scanned: `{total_exports}`",
        f"- New pages generated: `{generated}`",
        f"- Existing pages left in place: `{existing}`",
        f"- Existing pages with Apple Music URL backfilled: `{backfilled}`",
        f"- Parse errors needing review: `{len(parse_errors)}`",
        f"- Filename/header mismatches needing review: `{len(mismatches)}`",
        f"- Duplicate playlist dates reviewed automatically: `{len(duplicates)}`",
        f"- Future-dated exports skipped for now: `{len(future_dated)}`",
        "",
    ]

    if parse_errors:
        lines.extend(
            [
                "## Parse Errors",
                "",
                "These files could not be parsed as a standard seven-field SongShift export and were skipped:",
                "",
            ]
        )
        for filename, error in parse_errors:
            lines.append(f"- `{filename}` — {error}")
        lines.append("")

    if mismatches:
        lines.extend(
            [
                "## Filename/Header Mismatches",
                "",
                "These files parsed, but the filename date and the header playlist date did not agree:",
                "",
            ]
        )
        for filename, filename_date, header_date in mismatches:
            lines.append(
                f"- `{filename}` — filename implies `{filename_date}` but header says `{header_date}`"
            )
        lines.append("")

    if duplicates:
        lines.extend(
            [
                "## Duplicate Playlist Dates",
                "",
                "These playlist dates had more than one parsed export. A canonical source was chosen automatically, and the others were skipped:",
                "",
            ]
        )
        for playlist_date, exports, chosen in duplicates:
            lines.append(f"- `{playlist_date}` — chose `{chosen.path.name}`")
            for export in exports:
                label = "chosen" if export.path == chosen.path else "skipped"
                lines.append(
                    f"  - `{export.path.name}` exported `{export.exported_at}` ({label}, filename date `{export.filename_date}`)"
                )
        lines.append("")

    if future_dated:
        lines.extend(
            [
                "## Future-Dated Exports",
                "",
                "These exports have playlist dates after the current sweep date and were intentionally not published:",
                "",
            ]
        )
        for export in future_dated:
            lines.append(
                f"- `{export.path.name}` — header playlist date `{export.playlist_date}`"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = build_parser().parse_args()
    today = date.fromisoformat(args.today)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    parse_errors: list[tuple[str, str]] = []
    mismatches: list[tuple[str, str, str]] = []
    future_dated: list[ParsedExport] = []
    parsed_by_playlist_date: dict[str, list[ParsedExport]] = defaultdict(list)

    exports = iter_dated_exports(args.source_dir)
    for path, filename_date in exports:
        try:
            playlist = parse_songshift(path.read_text(encoding="utf-8-sig"), args.timezone)
        except Exception as exc:
            parse_errors.append((path.name, str(exc)))
            continue

        parsed = ParsedExport(
            path=path,
            filename_date=filename_date,
            playlist_date=playlist.playlist_date.isoformat(),
            exported_at=playlist.exported_at.isoformat(),
            content=playlist,
        )
        parsed_by_playlist_date[parsed.playlist_date].append(parsed)
        if parsed.filename_date != parsed.playlist_date:
            mismatches.append((parsed.path.name, parsed.filename_date, parsed.playlist_date))
        if playlist.playlist_date > today:
            future_dated.append(parsed)

    duplicates: list[tuple[str, list[ParsedExport], ParsedExport]] = []
    created: list[Path] = []
    existing: list[Path] = []
    backfilled: list[Path] = []

    for playlist_date in sorted(parsed_by_playlist_date):
        exports_for_date = parsed_by_playlist_date[playlist_date]
        if playlist_date > today.isoformat():
            continue

        chosen = pick_canonical(exports_for_date)
        if len(exports_for_date) > 1:
            duplicates.append((playlist_date, exports_for_date, chosen))

        target = args.output_dir / f"{playlist_date}.md"
        if target.exists():
            existing.append(target)
            if backfill_playlist_url(target, chosen.content):
                backfilled.append(target)
            continue

        target.write_text(render_published_entry(chosen.content), encoding="utf-8")
        created.append(target)

    write_review(
        args.review_path,
        today=today.isoformat(),
        total_exports=len(exports),
        generated=len(created),
        existing=len(existing),
        backfilled=len(backfilled),
        parse_errors=parse_errors,
        mismatches=mismatches,
        duplicates=duplicates,
        future_dated=sorted(future_dated, key=lambda item: item.playlist_date),
    )

    print(f"GENERATED {len(created)}")
    for path in created:
        print(path)
    print(f"EXISTING {len(existing)}")
    print(f"BACKFILLED {len(backfilled)}")
    print(f"REVIEW {args.review_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
