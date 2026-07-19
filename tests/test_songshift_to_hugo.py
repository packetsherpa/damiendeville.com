import unittest
from pathlib import Path

from scripts.songshift_to_hugo import (
    SongShiftFormatError,
    derive_playlist_url,
    parse_songshift,
    render_hugo,
)


FIXTURE = Path(__file__).parent / "fixtures" / "songshift-2026.07.19.txt"


class SongShiftImporterTests(unittest.TestCase):
    def test_parses_playlist_and_preserves_track_order(self):
        playlist = parse_songshift(FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(playlist.playlist_date.isoformat(), "2026-07-19")
        self.assertEqual(playlist.exported_at.isoformat(), "2026-07-18T22:41:00-04:00")
        self.assertEqual(playlist.service, "Apple Music")
        self.assertEqual(playlist.playlist_id, "pl.u-25V2ytKByDW")
        self.assertEqual(len(playlist.tracks), 10)
        self.assertEqual(playlist.tracks[0].title, "Version")
        self.assertEqual(playlist.tracks[0].artist, "Fugazi")
        self.assertEqual(playlist.tracks[0].album, "Red Medicine")
        self.assertEqual(playlist.tracks[-1].title, "Shove (Remastered)")

    def test_renders_reviewable_draft(self):
        playlist = parse_songshift(FIXTURE.read_text(encoding="utf-8"))
        rendered = render_hugo(playlist)

        self.assertIn('title: "Daily Playlist — July 19, 2026"', rendered)
        self.assertIn('publishDate: "2026-07-18"', rendered)
        self.assertIn("draft: true", rendered)
        self.assertIn('playlist_url: "https://music.apple.com/us/playlist/pl.u-25V2ytKByDW"', rendered)
        self.assertIn('album: "Red Medicine"', rendered)
        self.assertLess(rendered.index('title: "Version"'), rendered.index('title: "Kool Thing"'))

    def test_derives_apple_music_playlist_url_from_playlist_id(self):
        playlist = parse_songshift(FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual(
            derive_playlist_url(playlist),
            "https://music.apple.com/us/playlist/pl.u-25V2ytKByDW",
        )

    def test_rejects_ambiguous_track_rows(self):
        malformed = "\n".join(
            [
                "***playlist*** | SongShift | 07-18-2026 22:41 | 2026.07.19 | n/a | Apple Music | playlist-id",
                "Track | Artist | Album | applemusic",
            ]
        )

        with self.assertRaisesRegex(SongShiftFormatError, "expected five track fields"):
            parse_songshift(malformed)

    def test_rejects_duplicate_service_identifiers(self):
        duplicate = "\n".join(
            [
                "***playlist*** | SongShift | 07-18-2026 22:41 | 2026.07.19 | n/a | Apple Music | playlist-id",
                "One | Artist | Album | applemusic | 123",
                "Two | Artist | Album | applemusic | 123",
            ]
        )

        with self.assertRaisesRegex(SongShiftFormatError, "duplicate track identifier"):
            parse_songshift(duplicate)


if __name__ == "__main__":
    unittest.main()
