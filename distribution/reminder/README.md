# The tree reminds the founder — daily drop reminder

A local launchd agent (`city.banyan.drop-reminder`, plist in
`~/Library/LaunchAgents/`) runs `remind.sh` every day at 21:00 Asia/Dubai.
It shows a macOS notification with the night's episode, copies the caption
to the clipboard, opens `~/Downloads` (where the drop files are staged),
and plays a short in-character line from the tree's narrator. If the Mac is
asleep at 21:00, launchd fires it on next wake. After the final drop it
announces the season complete and unloads itself. Log:
`~/Library/Logs/banyan-reminder.log`.

Posting itself stays founder-only (operating rules) — this machine only
*reminds*; it never touches an account.

## Provenance (§7.2)

`voices/*.mp3` — written by the steward model (claude-fable-5), voiced by
kokoro-82M (voice `bm_fable`, the series' VO cast per
`genomes/sapling/voices.yaml`), local synthesis, $0.

Reinstall after moving the repo: fix the paths in `remind.sh` and the
plist, then `launchctl bootstrap gui/$(id -u)
~/Library/LaunchAgents/city.banyan.drop-reminder.plist`.
