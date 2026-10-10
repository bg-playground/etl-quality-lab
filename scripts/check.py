"""Run a source-to-target check; nonzero exit on data quality failure."""
import argparse
import json
from dataclasses import asdict
from pathlib import Path

from pipeline.quality import run_quality_check

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", choices=["clean", "defective"], default="clean")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
result = run_quality_check(root / "data" / args.dataset / "orders.csv",
                           root / "data/expected/fact_orders.csv")
print(json.dumps({**asdict(result), "passed": result.passed}, indent=2))
raise SystemExit(0 if result.passed else 1)
