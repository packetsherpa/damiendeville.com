#!/usr/bin/env python3
"""Sync newly dropped SongShift exports into published Hugo daily playlist pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.songshift_to_hugo import PlaylistExport, derive_playlist_url, parse_songshift


DATE_EXPORT_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}.*\.txt$", re.IGNORECASE)
DEFAULT_STATE_FILE = Path(".playlist-sync-state.json")


@dataclass(frozen=True)
class SyncSummary:
    initialized: bool
    created: tuple[Path, ...]
    updated: tuple[Path, ...]
    skipped: tuple[str, ...]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("~/Documents/playlists").expanduser(),
        help="Directory containing SongShift exports.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("content/music/daily"),
        help="Directory where Hugo daily playlist pages live.",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=DEFAULT_STATE_FILE,
        help="Local JSON file tracking which exports have already been seen.",
    )
    parser.add_argument(
        "--timezone",
        default="America/New_York",
        help="Timezone used when parsing SongShift exports.",
    )
    parser.add_argument(
        "--import-existing",
        action="store_true",
        help="Process all matching exports even if no state file exists yet.",
    )
    return parser


def state_signature(path: Path) -> dict[str, int]:
    stat = path.stat()
    return {"mtime_ns": stat.st_mtime_ns, "size": stat.st_size}


def load_state(path: Path) -> dict[str, dict[str, int]]:
    if not path.exists():
        return {"seen_exports": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, dict[str, int]]) -> None:
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_export_paths(source_dir: Path) -> list[Path]:
    return sorted(
        path for path in source_dir.iterdir() if path.is_file() and DATE_EXPORT_RE.match(path.name)
    )


def unique_artists(playlist: PlaylistExport, limit: int = 3) -> list[str]:
    artists: list[str] = []
    for track in playlist.tracks:
        if track.artist not in artists:
            artists.append(track.artist)
        if len(artists) == limit:
            break
    return artists


def describe_artists(artists: list[str]) -> str:
    if not artists:
        return "the day’s sequence"
    if len(artists) == 1:
        return artists[0]
    if len(artists) == 2:
        return f"{artists[0]} and {artists[1]}"
    return f"{artists[0]}, {artists[1]}, and {artists[2]}"


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_published_entry(playlist: PlaylistExport) -> str:
    display_date = (
        f"{playlist.playlist_date.strftime('%B')} "
        f"{playlist.playlist_date.day}, {playlist.playlist_date.year}"
    )
    description = (
        f"Ten tracks shared on {display_date}, moving through "
        f"{describe_artists(unique_artists(playlist))}."
    )
    intro = (
        f'This playlist captures what was in rotation on {display_date}, with '
        f'{yaml_string(playlist.tracks[0].title)} by {playlist.tracks[0].artist} setting the tone.'
    )
    why = (
        "These ten songs stay in the exported order from SongShift, so this page "
        "reflects the sequence that was shared that day."
    )

    lines = [
        "---",
        f"title: {yaml_string(f'Daily Playlist — {display_date}')}",
        f"date: {playlist.playlist_date.isoformat()}",
        f"publishDate: {playlist.exported_at.date().isoformat()}",
        "draft: false",
        f"description: {yaml_string(description)}",
        'music_kind: "Daily playlist"',
        f"playlist_url: {yaml_string(derive_playlist_url(playlist))}",
        'threads_url: ""',
        'image: ""',
        'image_alt: ""',
        "tags:",
        "  - playlist",
        "tracks:",
    ]

    for track in playlist.tracks:
        lines.extend(
            [
                f"  - title: {yaml_string(track.title)}",
                f"    artist: {yaml_string(track.artist)}",
                f"    album: {yaml_string(track.album)}",
            ]
        )

    lines.extend(
        [
            "source:",
            f"  application: {yaml_string(playlist.source_name)}",
            f"  exported_at: {yaml_string(playlist.exported_at.isoformat())}",
            f"  service: {yaml_string(playlist.service)}",
            f"  playlist_id: {yaml_string(playlist.playlist_id)}",
            "---",
            "",
            intro,
            "",
            "<!--more-->",
            "",
            "## Why these tracks",
            "",
            why,
            "",
        ]
    )
    return "\n".join(lines)


def backfill_playlist_url(page_path: Path, playlist: PlaylistExport) -> bool:
    playlist_url = derive_playlist_url(playlist)
    if not playlist_url:
        return False

    text = page_path.read_text(encoding="utf-8")
    updated = re.sub(
        r'^playlist_url:\s*""\s*$',
        f'playlist_url: "{playlist_url}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if updated == text:
        return False
    page_path.write_text(updated, encoding="utf-8")
    return True


def choose_latest_exports(
    paths: list[Path],
    timezone: str,
) -> tuple[dict[str, tuple[Path, PlaylistExport]], list[str]]:
    by_date: dict[str, tuple[Path, PlaylistExport]] = {}
    skipped: list[str] = []

    for path in paths:
        playlist = parse_songshift(path.read_text(encoding="utf-8-sig"), timezone)
        iso_date = playlist.playlist_date.isoformat()
        current = by_date.get(iso_date)
        if current is None or playlist.exported_at > current[1].exported_at:
            if current is not None:
                skipped.append(
                    f"{current[0].name}: superseded by newer export {path.name} for {iso_date}"
                )
            by_date[iso_date] = (path, playlist)
        else:
            skipped.append(f"{path.name}: older export ignored for {iso_date}")

    return by_date, skipped


def initialize_state(source_dir: Path, state_file: Path) -> SyncSummary:
    exports = iter_export_paths(source_dir)
    state = {"seen_exports": {str(path): state_signature(path) for path in exports}}
    save_state(state_file, state)
    return SyncSummary(
        initialized=True,
        created=(),
        updated=(),
        skipped=(f"Initialized state with {len(exports)} existing exports.",),
    )


def sync_playlists(
    *,
    source_dir: Path,
    output_dir: Path,
    state_file: Path,
    timezone: str,
    import_existing: bool,
) -> SyncSummary:
    output_dir.mkdir(parents=True, exist_ok=True)
    state = load_state(state_file)
    seen = state.setdefault("seen_exports", {})

    if not state_file.exists() and not import_existing:
        return initialize_state(source_dir, state_file)

    export_paths = iter_export_paths(source_dir)
    changed_paths = [
        path for path in export_paths if seen.get(str(path)) != state_signature(path)
    ]

    if not changed_paths:
        return SyncSummary(
            initialized=False,
            created=(),
            updated=(),
            skipped=("No new playlist exports found.",),
        )

    selected, skipped = choose_latest_exports(changed_paths, timezone)
    created: list[Path] = []
    updated: list[Path] = []

    for iso_date, (source_path, playlist) in selected.items():
        target = output_dir / f"{iso_date}.md"
        if target.exists():
            if backfill_playlist_url(target, playlist):
                updated.append(target)
            else:
                skipped.append(f"{target.name}: page already exists; left content unchanged")
        else:
            target.write_text(render_published_entry(playlist), encoding="utf-8")
            created.append(target)
        seen[str(source_path)] = state_signature(source_path)

    for path in changed_paths:
        seen[str(path)] = state_signature(path)

    save_state(state_file, state)
    return SyncSummary(
        initialized=False,
        created=tuple(created),
        updated=tuple(updated),
        skipped=tuple(skipped),
    )


def main() -> int:
    args = build_parser().parse_args()
    summary = sync_playlists(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        state_file=args.state_file,
        timezone=args.timezone,
        import_existing=args.import_existing,
    )

    if summary.initialized:
        print(summary.skipped[0])
        return 0

    for path in summary.created:
        print(f"CREATED {path}")
    for path in summary.updated:
        print(f"UPDATED {path}")
    for line in summary.skipped:
        print(f"SKIPPED {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
