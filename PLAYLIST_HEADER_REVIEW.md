# Playlist Header Review

This report was generated during the dated-playlist backfill sweep so that questionable exports could be reviewed later without halting page generation.

## Summary

- Sweep date basis: `2026-07-19`
- Dated exports scanned: `568`
- New pages generated: `0`
- Existing pages left in place: `530`
- Existing pages with Apple Music URL backfilled: `0`
- Parse errors needing review: `34`
- Filename/header mismatches needing review: `2`
- Duplicate playlist dates reviewed automatically: `2`
- Future-dated exports skipped for now: `2`

## Parse Errors

These files could not be parsed as a standard seven-field SongShift export and were skipped:

- `2024.10.27.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2024.11.19.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2025.01.26.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2025.02.23.txt` — Line 11: expected five track fields, found 6.
- `2025.03.30.txt` — Line 2: expected a seven-field SongShift playlist header.
- `2025.04.17.txt` — Line 2: expected a seven-field SongShift playlist header.
- `2025.04.26.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2025.05.01.txt` — Line 14: expected five track fields, found 1.
- `2025.06.08.txt` — Line 1: invalid export timestamp ''.
- `2025.06.19.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2025.06.22.txt` — Line 1: invalid playlist date '2025.06.22b'.
- `2025.06.23.txt` — Line 5: expected five track fields, found 6.
- `2026.02.15.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.16.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.17.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.18.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.19.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.20.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.21.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.22.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.23.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.24.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.25.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.26.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.27.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.02.28.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.02.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.03.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.04.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.05.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.06.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.07.txt` — Line 1: expected a seven-field SongShift playlist header.
- `2026.03.28.txt` — Line 1: invalid playlist date 'New'.
- `2026.04.17.txt` — Line 2: expected a seven-field SongShift playlist header.

## Filename/Header Mismatches

These files parsed, but the filename date and the header playlist date did not agree:

- `2025.05.08.txt` — filename implies `2025-05-08` but header says `2025-05-07`
- `2025.10.23.txt` — filename implies `2025-10-23` but header says `2025-10-22`

## Duplicate Playlist Dates

These playlist dates had more than one parsed export. A canonical source was chosen automatically, and the others were skipped:

- `2025-05-07` — chose `2025.05.07.txt`
  - `2025.05.07.txt` exported `2025-05-07T08:07:00-04:00` (chosen, filename date `2025-05-07`)
  - `2025.05.08.txt` exported `2025-05-08T08:44:00-04:00` (skipped, filename date `2025-05-08`)
- `2025-10-22` — chose `2025.10.22.txt`
  - `2025.10.22.txt` exported `2025-10-22T08:46:00-04:00` (chosen, filename date `2025-10-22`)
  - `2025.10.23.txt` exported `2025-10-23T12:45:00-04:00` (skipped, filename date `2025-10-23`)

## Future-Dated Exports

These exports have playlist dates after the current sweep date and were intentionally not published:

- `2026.09.27.txt` — header playlist date `2026-09-27`
- `2026.10.29.txt` — header playlist date `2026-10-29`
