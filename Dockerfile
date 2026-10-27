# simulforge - streaming speech-to-speech simultaneous interpretation
FROM python:3.12-slim

WORKDIR /app

# pure-Python, zero runtime dependencies
COPY simulforge/ ./simulforge/
COPY tests/ ./tests/
COPY README.md pyproject.toml LICENSE ./

ENV PYTHONUNBUFFERED=1

EXPOSE 8432

# default: serve the interpretation engine over HTTP
CMD ["python", "-m", "simulforge.cli", "serve", "--host", "0.0.0.0", "--port", "8432"]
