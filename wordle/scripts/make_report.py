# Run with: python scripts/make_report.py --summary logs/summary.csv --jsonl logs/results.jsonl --provider ollama --model llama3.1:8b --output logs/report.md
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Markdown report from benchmark artifacts.")
    parser.add_argument("--summary", required=True, help="Path to the CSV summary file.")
    parser.add_argument("--jsonl", required=True, help="Path to the per-game JSONL log.")
    parser.add_argument("--provider", required=True, help="LLM provider name.")
    parser.add_argument("--model", required=True, help="LLM model identifier.")
    parser.add_argument("--output", required=True, help="Destination Markdown report path.")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def load_summary(path: Path) -> Dict[str, Any]:
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        fail(f"Summary CSV not found at '{path}'.")  # pragma: no cover
    except Exception as exc:  # noqa: BLE001
        fail(f"Failed to read summary CSV '{path}': {exc}")  # pragma: no cover

    if df.empty:
        fail(f"Summary CSV '{path}' is empty.")

    row = df.iloc[0].to_dict()
    required_keys = {"games", "wins", "win_rate_percent", "average_turns", "average_duration_s"}
    missing = required_keys - row.keys()
    if missing:
        fail(f"Summary CSV is missing required columns: {', '.join(sorted(missing))}")
    return row


def load_samples(path: Path, limit: int = 3) -> List[Dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        fail(f"JSONL log not found at '{path}'.")
    except Exception as exc:  # noqa: BLE001
        fail(f"Failed to read JSONL log '{path}': {exc}")

    records: List[Dict[str, Any]] = []
    for idx, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            fail(f"Malformed JSON on line {idx + 1} in '{path}': {exc}")
        if len(records) >= limit:
            break

    if not records:
        fail(f"No JSON records found in '{path}'.")
    return records


def build_markdown(
    provider: str,
    model: str,
    summary: Dict[str, Any],
    samples: List[Dict[str, Any]],
    summary_path: Path,
    jsonl_path: Path,
) -> str:
    lines = [
        "# Wordle Benchmark Report",
        "",
        f"- Provider: `{provider}`",
        f"- Model: `{model}`",
        f"- Summary CSV: `{summary_path}`",
        f"- JSONL Log: `{jsonl_path}`",
        "",
        "## Aggregate Results",
        f"- Games: {int(summary['games'])}",
        f"- Wins: {int(summary['wins'])}",
        f"- Win rate: {summary['win_rate_percent']:.2f}%",
        f"- Average turns: {summary['average_turns']:.2f}",
        f"- Average duration (s): {summary['average_duration_s']:.2f}",
        "",
        "## Sample Games",
        "```json",
    ]

    for sample in samples:
        lines.append(json.dumps(sample, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("_Report generated automatically._")
    return "\n".join(lines)


def write_report(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    summary_path = Path(args.summary).resolve()
    jsonl_path = Path(args.jsonl).resolve()
    output_path = Path(args.output).resolve()

    summary = load_summary(summary_path)
    samples = load_samples(jsonl_path)

    report = build_markdown(args.provider, args.model, summary, samples, summary_path, jsonl_path)
    write_report(output_path, report)
    print(f"Markdown report saved to: {output_path}")


if __name__ == "__main__":
    main()
