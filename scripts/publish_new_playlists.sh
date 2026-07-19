#!/bin/zsh
set -euo pipefail

script_dir=${0:A:h}
repo_dir=${script_dir:h}

if [[ $# -gt 1 ]]; then
  print -u2 "usage: $0 [--dry-run]"
  exit 2
fi

dry_run=0
if [[ ${1:-} == "--dry-run" ]]; then
  dry_run=1
fi

cd "$repo_dir"

preexisting_changes=$(git status --porcelain --untracked-files=all)
if [[ -n "$preexisting_changes" ]]; then
  print -u2 "Refusing to auto-publish because the repository is not clean."
  print -u2 "$preexisting_changes"
  exit 1
fi

git pull --ff-only

sync_output=$(python3 scripts/sync_daily_playlists.py)
print -- "$sync_output"

playlist_files=("${(@f)$(git ls-files --others --modified --exclude-standard -- content/music/daily)}")
if (( ${#playlist_files} == 0 )); then
  print -- "No playlist page changes to publish."
  exit 0
fi

python3 -m unittest tests.test_songshift_to_hugo tests.test_sync_daily_playlists
hugo --gc --minify --panicOnWarning

if (( dry_run == 1 )); then
  print -- "Dry run complete; skipping git add/commit/push."
  exit 0
fi

git add -- "${playlist_files[@]}"

if (( ${#playlist_files} == 1 )); then
  playlist_name=${playlist_files[1]:t:r}
  commit_message="Publish daily playlist for ${playlist_name}"
else
  commit_message="Publish ${#playlist_files} daily playlists"
fi

git commit -m "$commit_message"
git push origin main
