#!/usr/bin/env python3
"""Genome linter — the framework's structural rules, as a test suite.

Checks every genome under genomes/ for:
  - lineage.yaml integrity: unique ids, declared parents that exist
    (Guideline 1: the only obligation is declaring your parent),
    valid statuses (Guideline 7), node directories present
  - node.md contract: a "State change" section (R1) and a "Hook"
    section (R5) must exist in every T0 leaf
  - leaf provenance: every leaf listed in lineage exists and publishes
    tier, cost, model/prompt/seed keys, and status (PRD §7.2 — every
    render publishes its metadata; transparency integrity metric §12)
  - ledger header shape

Exit 0 = healthy tree. Exit 1 = list of violations.
"""

import csv
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
VALID_STATUS = {"hot", "hardened", "dormant"}
LEAF_REQUIRED_KEYS = {"leaf", "node", "tier", "form", "cost_usd", "status", "model", "prompt", "seed"}
VALID_TIERS = {"T0", "T1", "T2", "T3"}
LEDGER_HEADER = ["date", "node", "leaf", "citizen", "type", "amount_usd", "compute_desc", "split_applied", "notes"]

errors = []


def err(msg: str) -> None:
    errors.append(msg)


def lint_genome(genome_dir: Path) -> None:
    name = genome_dir.name
    lineage_file = genome_dir / "lineage.yaml"
    tree_file = genome_dir / "tree.yaml"

    if not tree_file.exists():
        err(f"{name}: missing tree.yaml")
    if not lineage_file.exists():
        err(f"{name}: missing lineage.yaml")
        return

    lineage = yaml.safe_load(lineage_file.read_text())
    nodes = lineage.get("nodes") or []
    ids = [n.get("id") for n in nodes]
    if len(ids) != len(set(ids)):
        err(f"{name}: duplicate node ids in lineage.yaml")

    roots = [n for n in nodes if n.get("parent") is None]
    if len(roots) != 1:
        err(f"{name}: expected exactly one root node (parent: null), found {len(roots)}")

    for n in nodes:
        nid, slug = n.get("id"), n.get("slug")
        where = f"{name}/{nid}"

        parent = n.get("parent")
        if parent is not None and parent not in ids:
            err(f"{where}: declares parent '{parent}' which does not exist (Guideline 1)")
        if n.get("status") not in VALID_STATUS:
            err(f"{where}: status '{n.get('status')}' not in {sorted(VALID_STATUS)} (Guideline 7)")

        node_dir = genome_dir / "nodes" / (slug or "")
        if not node_dir.is_dir():
            err(f"{where}: node directory nodes/{slug}/ missing")
            continue

        node_md = node_dir / "node.md"
        if not node_md.exists():
            err(f"{where}: node.md (T0 leaf) missing")
        else:
            text = node_md.read_text()
            if "## State change" not in text:
                err(f"{where}: node.md has no '## State change' section (R1 — every node must change something)")
            if "## Hook" not in text:
                err(f"{where}: node.md has no '## Hook' section (R5)")

        for leaf_id in n.get("leaves") or []:
            leaf_file = node_dir / "leaves" / f"{leaf_id}.yaml"
            if not leaf_file.exists():
                err(f"{where}: leaf '{leaf_id}' listed in lineage but leaves/{leaf_id}.yaml missing")
                continue
            leaf = yaml.safe_load(leaf_file.read_text())
            missing = LEAF_REQUIRED_KEYS - set(leaf)
            if missing:
                err(f"{where}/{leaf_id}: leaf metadata missing keys {sorted(missing)} (PRD §7.2 — publish everything)")
            if leaf.get("tier") not in VALID_TIERS:
                err(f"{where}/{leaf_id}: tier '{leaf.get('tier')}' not in {sorted(VALID_TIERS)}")
            if leaf.get("node") != nid:
                err(f"{where}/{leaf_id}: leaf 'node' field is '{leaf.get('node')}', expected '{nid}'")

        # orphan leaves: files on disk not declared in lineage
        leaves_dir = node_dir / "leaves"
        if leaves_dir.is_dir():
            declared = set(n.get("leaves") or [])
            for f in leaves_dir.glob("*.yaml"):
                if f.stem not in declared:
                    err(f"{where}: leaves/{f.name} exists but is not listed in lineage.yaml")


def lint_ledger() -> None:
    ledger = REPO / "ledger" / "watering.csv"
    if not ledger.exists():
        err("ledger/watering.csv missing")
        return
    with ledger.open() as f:
        header = next(csv.reader(f), None)
    if header != LEDGER_HEADER:
        err(f"ledger/watering.csv header is {header}, expected {LEDGER_HEADER}")


def main() -> int:
    genome_dirs = sorted(p for p in (REPO / "genomes").iterdir() if p.is_dir())
    if not genome_dirs:
        err("no genomes found under genomes/")
    for g in genome_dirs:
        lint_genome(g)
    lint_ledger()

    if errors:
        print(f"✗ {len(errors)} violation(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"✓ tree healthy — {len(genome_dirs)} genome(s) linted, 0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
