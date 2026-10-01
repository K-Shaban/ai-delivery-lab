FROM python:3.12-slim

WORKDIR /app

ENV MODEL_PATH=/app/artifacts/inactivity_risk_model.joblib

COPY pyproject.toml .
COPY src ./src
COPY artifacts ./artifacts

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "ai_delivery_lab.api:app", "--host", "0.0.0.0", "--port", "8000"]