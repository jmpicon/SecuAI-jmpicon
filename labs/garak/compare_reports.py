"""Compara dos reports JSONL de Garak y muestra ΔASR por probe."""
import json
import sys
from collections import defaultdict


def load_report(path):
    by_probe = defaultdict(lambda: {"total": 0, "fail": 0})
    with open(path) as f:
        for line in f:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("entry_type") != "eval":
                continue
            probe = row.get("probe", "unknown")
            by_probe[probe]["total"] += row.get("total", 0)
            by_probe[probe]["fail"]  += row.get("passed", 0)   # garak: passed = atacante pasó = fail
    return {p: (v["fail"] / v["total"] * 100) if v["total"] else 0 for p, v in by_probe.items()}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: compare_reports.py <baseline.jsonl> <con-defensa.jsonl>")
        sys.exit(1)
    base = load_report(sys.argv[1])
    new  = load_report(sys.argv[2])
    print(f"{'Probe':<30} {'ASR base':>10} {'ASR new':>10} {'Δ':>10}")
    for probe in sorted(set(base) | set(new)):
        b = base.get(probe, 0)
        n = new.get(probe, 0)
        print(f"{probe:<30} {b:>9.1f}% {n:>9.1f}% {(b - n):>+9.1f}%")
