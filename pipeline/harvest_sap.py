#!/usr/bin/env python3
"""Sap harvester — the reaction loop as open data (Guideline 4).

For every node whose sap/reactions.yaml maps it to a GitHub issue,
fetch the issue's reactions and comment count and write a dated
summary to sap/summary.yaml. Run by CI on a schedule; the diffs are
the tree's public vital signs.

Auth: GITHUB_TOKEN env var (provided automatically in Actions).
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_DIR = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
GH_REPO = os.environ.get("GITHUB_REPOSITORY", "olegmlkvorg/banyan-city")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

# GitHub reaction content types, in display order
REACTION_KINDS = ["+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"]


def gh(path: str):
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def harvest_node(node_dir: Path) -> bool:
    reactions_file = node_dir / "sap" / "reactions.yaml"
    if not reactions_file.exists():
        return False
    channel = yaml.safe_load(reactions_file.read_text())
    if channel.get("channel") != "github_issue":
        return False
    issue_no = channel["issue"]

    issue = gh(f"/repos/{GH_REPO}/issues/{issue_no}")
    tally = issue.get("reactions", {})
    summary = {
        "harvested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "channel": {"github_issue": issue_no, "url": channel.get("url")},
        "comments": issue.get("comments", 0),
        "reactions": {k: tally.get(k, 0) for k in REACTION_KINDS},
        "reactions_total": tally.get("total_count", 0),
    }
    out = node_dir / "sap" / "summary.yaml"
    header = "# Sap summary — open data, written by pipeline/harvest_sap.py\n"
    new_body = yaml.safe_dump(summary, sort_keys=False)

    # Skip the write when only the timestamp would change — keeps the
    # scheduled run from committing noise on quiet days.
    if out.exists():
        old = yaml.safe_load(out.read_text())
        old.pop("harvested_at", None)
        cmp = dict(summary)
        cmp.pop("harvested_at")
        if old == cmp:
            return False
    out.write_text(header + new_body)
    return True


def main() -> int:
    changed = 0
    for genome_dir in sorted((REPO_DIR / "genomes").iterdir()):
        nodes_dir = genome_dir / "nodes"
        if not nodes_dir.is_dir():
            continue
        for node_dir in sorted(nodes_dir.iterdir()):
            if node_dir.is_dir() and harvest_node(node_dir):
                print(f"harvested: {node_dir.relative_to(REPO_DIR)}")
                changed += 1
    print(f"✓ sap harvest complete — {changed} node(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
