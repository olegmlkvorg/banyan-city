#!/bin/bash
# The tree reminds the founder to post tonight's episode — daily 21:00 via
# launchd (city.banyan.drop-reminder). Speaks in the show's narrator voice,
# puts the caption on the clipboard, opens Downloads. Retires itself after
# the season is fully dropped.
REPO="/Users/artovonkugler/banyan-city"
V="$REPO/distribution/reminder/voices"
today=$(date +%Y-%m-%d)

case "$today" in
  2026-07-22) EP=ep3; FILE="banyan-003b-episode.mp4"; TITLE="Post Sapling ep 3 — One Leaf for Yes"
    CAP='He asked if I can hear him. One leaf for yes. Nothing for no.
"Did you MEAN to hit my head with that fig?" …long pause… one leaf.
Sapling ep 3 · banyan.city
#anime #aianimation #wholesome' ;;
  2026-07-23) EP=ep4; FILE="banyan-004-episode.mp4"; TITLE="Post Sapling ep 4 — Shade"
    CAP='Naming a town is hard when the founding committee is a goblin and a plant.
"Newhaven?" No leaf. "Greenrest?" Nothing. "…it'"'"'s just shade." BOTH LEAVES.
Sapling ep 4 · banyan.city
#anime #aianimation #cozy' ;;
  2026-07-24) EP=ep5; FILE="banyan-005-episode.mp4"; TITLE="Post Sapling ep 5 — The Assessor"
    CAP='The tax man came to assess a town with one shack, three rocks, and a tree that answers questions. He counted the rocks individually.
"Occupation?" …one leaf. "Noted."
Sapling ep 5 · banyan.city
#anime #aianimation #isekai' ;;
  2026-07-25) EP=ep6; FILE="banyan-006a-episode.mp4"; TITLE="Post Sapling ep 6 — The Miracle Clause"
    CAP='The verdict: the talking tree is legally a SHRINE. The fugitive goblin is now its official keeper. One catch — they owe the kingdom a verified miracle by the full moon.
Sapling ep 6 · full season at banyan.city
#anime #aianimation #interactivefiction' ;;
  2026-07-26) EP=ep7; FILE="banyan-007a-episode.mp4"; TITLE="Post Sapling ep 7 — SEASON FINALE"
    CAP='They rehearsed a miracle for two weeks. The wind ruined it in four seconds. What happened next was not rehearsed.
Season finale · whole season free at banyan.city · the story branches — you pick what happens next
#anime #aianimation #interactivefiction' ;;
  *) EP=done; FILE=""; TITLE="Season fully dropped"
    CAP='' ;;
esac

if [ "$EP" = "done" ]; then
  afplay "$V/done.mp3" 2>/dev/null
  osascript -e 'display notification "The season is in the world. Check the sap. Reminder retiring." with title "🌳 Banyan City" sound name "Glass"'
  launchctl unload ~/Library/LaunchAgents/city.banyan.drop-reminder.plist 2>/dev/null
  exit 0
fi

printf '%s' "$CAP" | pbcopy
osascript -e "display notification \"$FILE → Downloads. Caption on clipboard. AI label ON.\" with title \"🌳 $TITLE\" sound name \"Glass\""
open ~/Downloads
afplay "$V/$EP.mp3" 2>/dev/null
