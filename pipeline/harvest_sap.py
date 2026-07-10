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
import re
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


def parse_screening_issue(body: str):
    """Parse a screening issue-form body into (leaf_id, scores, note)."""
    sections = dict(re.findall(r"### ([^\n]+)\n\n(.*?)(?=\n### |\Z)", body or "", re.S))
    leaf = None
    scores = {}
    note = ""
    for label, answer in sections.items():
        answer = answer.strip()
        if label.startswith("Leaf ID"):
            leaf = answer.split()[0] if answer else None
        elif label.startswith("The wince"):
            note = "" if answer == "_No response_" else answer
        else:
            m = re.match(r"([1-5])", answer)
            if m:
                key = label.split(" (")[0].strip().lower().replace(" ", "_")
                scores[key] = int(m.group(1))
    return leaf, scores, note


def harvest_screening(genome_dirs: list) -> int:
    """Tally screening-form issues into each node's sap/screening.yaml."""
    issues = gh(f"/repos/{GH_REPO}/issues?labels=screening&state=all&per_page=100")
    by_leaf = {}
    for issue in issues:
        leaf, scores, note = parse_screening_issue(issue.get("body", ""))
        if not leaf or not scores:
            continue
        entry = by_leaf.setdefault(leaf, {"ratings": 0, "sums": {}, "winces": []})
        entry["ratings"] += 1
        for k, v in scores.items():
            entry["sums"][k] = entry["sums"].get(k, 0) + v
        if note:
            entry["winces"].append({"issue": issue["number"], "note": note[:500]})

    changed = 0
    for genome_dir in genome_dirs:
        lineage = yaml.safe_load((genome_dir / "lineage.yaml").read_text())
        for node in lineage["nodes"]:
            leaves = {l: by_leaf[l] for l in (node.get("leaves") or []) if l in by_leaf}
            if not leaves:
                continue
            summary = {
                "harvested_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "leaves": {
                    leaf: {
                        "ratings": e["ratings"],
                        "means": {k: round(s / e["ratings"], 2) for k, s in e["sums"].items()},
                        "winces": e["winces"],
                    }
                    for leaf, e in leaves.items()
                },
            }
            out = genome_dir / "nodes" / node["slug"] / "sap" / "screening.yaml"
            header = "# Screening summary — open data, written by pipeline/harvest_sap.py\n"
            if out.exists():
                old = yaml.safe_load(out.read_text())
                old.pop("harvested_at", None)
                cmp = dict(summary)
                cmp.pop("harvested_at")
                if old == cmp:
                    continue
            out.write_text(header + yaml.safe_dump(summary, sort_keys=False))
            print(f"screening: {out.relative_to(REPO_DIR)}")
            changed += 1
    return changed


def main() -> int:
    changed = 0
    genome_dirs = [p for p in sorted((REPO_DIR / "genomes").iterdir()) if (p / "lineage.yaml").exists()]
    for genome_dir in genome_dirs:
        nodes_dir = genome_dir / "nodes"
        for node_dir in sorted(nodes_dir.iterdir()):
            if node_dir.is_dir() and harvest_node(node_dir):
                print(f"harvested: {node_dir.relative_to(REPO_DIR)}")
                changed += 1
    changed += harvest_screening(genome_dirs)
    print(f"✓ sap harvest complete — {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
