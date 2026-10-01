from datetime import datetime, timezone
from pathlib import Path
import json
import os


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOG_PATH = Path(
    os.getenv(
        "PREDICTION_LOG_PATH",
        PROJECT_ROOT / "artifacts" / "prediction_log.jsonl",
    )
)


def log_prediction(at_risk: int, risk_probability: float) -> None:
    """Record a model prediction for basic monitoring."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "at_risk": int(at_risk),
        "risk_probability": float(risk_probability),
    }

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

def prediction_summary() -> dict[str, float | int]:
    """Summarize recorded model predictions."""
    if not LOG_PATH.exists():
        return {
            "prediction_count": 0,
            "average_risk_probability": 0.0,
            "at_risk_count": 0,
        }

    records = []

    with LOG_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    if not records:
        return {
            "prediction_count": 0,
            "average_risk_probability": 0.0,
            "at_risk_count": 0,
        }

    return {
        "prediction_count": len(records),
        "average_risk_probability": sum(
            record["risk_probability"] for record in records
        ) / len(records),
        "at_risk_count": sum(
            record["at_risk"] for record in records
        ),
    }