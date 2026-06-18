import argparse
import json
from pathlib import Path

from rag_engine.evals.full_eval import run_full_eval


DEFAULT_DATASET = Path("data/evals/full_eval.jsonl")
DEFAULT_RESULTS_DIR = Path("data/evals/results")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the full RAG eval harness.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--results-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--previous-report", default=None)
    args = parser.parse_args()

    previous_report = Path(args.previous_report) if args.previous_report else None
    report = run_full_eval(
        dataset_path=Path(args.dataset),
        results_dir=Path(args.results_dir),
        previous_report_path=previous_report,
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
