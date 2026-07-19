import tempfile
import unittest
from pathlib import Path

from scripts.sync_daily_playlists import sync_playlists


FIXTURE = Path(__file__).parent / "fixtures" / "songshift-2026.07.19.txt"


def write_export(target: Path, *, export_stamp: str, playlist_stamp: str) -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    parts = [field.strip() for field in lines[0].split("|")]
    parts[2] = export_stamp
    parts[3] = playlist_stamp
    lines[0] = " | ".join(parts)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


class SyncDailyPlaylistsTests(unittest.TestCase):
    def test_first_run_initializes_state_without_importing_existing_exports(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_dir = root / "playlists"
            output_dir = root / "content" / "music" / "daily"
            state_file = root / ".playlist-sync-state.json"
            source_dir.mkdir(parents=True)
            write_export(
                source_dir / "2026.07.19.txt",
                export_stamp="07-18-2026 22:41",
                playlist_stamp="2026.07.19",
            )

            summary = sync_playlists(
                source_dir=source_dir,
                output_dir=output_dir,
                state_file=state_file,
                timezone="America/New_York",
                import_existing=False,
            )

            self.assertTrue(summary.initialized)
            self.assertTrue(state_file.exists())
            self.assertFalse((output_dir / "2026-07-19.md").exists())

    def test_import_existing_creates_a_published_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_dir = root / "playlists"
            output_dir = root / "content" / "music" / "daily"
            state_file = root / ".playlist-sync-state.json"
            source_dir.mkdir(parents=True)
            write_export(
                source_dir / "2026.07.19.txt",
                export_stamp="07-18-2026 22:41",
                playlist_stamp="2026.07.19",
            )

            summary = sync_playlists(
                source_dir=source_dir,
                output_dir=output_dir,
                state_file=state_file,
                timezone="America/New_York",
                import_existing=True,
            )

            page = output_dir / "2026-07-19.md"
            self.assertEqual(summary.created, (page,))
            rendered = page.read_text(encoding="utf-8")
            self.assertIn('draft: false', rendered)
            self.assertIn(
                'playlist_url: "https://music.apple.com/us/playlist/pl.u-25V2ytKByDW"',
                rendered,
            )

    def test_new_export_after_bootstrap_creates_only_the_new_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_dir = root / "playlists"
            output_dir = root / "content" / "music" / "daily"
            state_file = root / ".playlist-sync-state.json"
            source_dir.mkdir(parents=True)
            write_export(
                source_dir / "2026.07.19.txt",
                export_stamp="07-18-2026 22:41",
                playlist_stamp="2026.07.19",
            )

            sync_playlists(
                source_dir=source_dir,
                output_dir=output_dir,
                state_file=state_file,
                timezone="America/New_York",
                import_existing=False,
            )

            write_export(
                source_dir / "2026.07.20.txt",
                export_stamp="07-19-2026 07:00",
                playlist_stamp="2026.07.20",
            )

            summary = sync_playlists(
                source_dir=source_dir,
                output_dir=output_dir,
                state_file=state_file,
                timezone="America/New_York",
                import_existing=False,
            )

            self.assertEqual(len(summary.created), 1)
            self.assertEqual(summary.created[0].name, "2026-07-20.md")
            self.assertFalse((output_dir / "2026-07-19.md").exists())

    def test_existing_page_gets_playlist_url_backfill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_dir = root / "playlists"
            output_dir = root / "content" / "music" / "daily"
            state_file = root / ".playlist-sync-state.json"
            source_dir.mkdir(parents=True)
            output_dir.mkdir(parents=True)
            write_export(
                source_dir / "2026.07.19.txt",
                export_stamp="07-18-2026 22:41",
                playlist_stamp="2026.07.19",
            )
            page = output_dir / "2026-07-19.md"
            page.write_text(
                "\n".join(
                    [
                        "---",
                        'title: "Daily Playlist — July 19, 2026"',
                        "date: 2026-07-19",
                        "publishDate: 2026-07-18",
                        "draft: false",
                        'description: "Test entry."',
                        'music_kind: "Daily playlist"',
                        'playlist_url: ""',
                        'threads_url: ""',
                        'image: ""',
                        'image_alt: ""',
                        "---",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            summary = sync_playlists(
                source_dir=source_dir,
                output_dir=output_dir,
                state_file=state_file,
                timezone="America/New_York",
                import_existing=True,
            )

            self.assertEqual(summary.updated, (page,))
            self.assertIn(
                'playlist_url: "https://music.apple.com/us/playlist/pl.u-25V2ytKByDW"',
                page.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
