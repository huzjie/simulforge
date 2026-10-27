# Getting started

## 1. Smoke test

```bash
python -m simulforge.cli doctor --skill 0.8
```

## 2. Interpret one utterance

```bash
python -m simulforge.cli interpret hello-world --speaker-id alice
```

## 3. Train and benchmark

```bash
python -m simulforge.cli train --steps 24
python -m simulforge.cli bench
```

## 4. Serve over HTTP

```bash
python -m simulforge.cli serve --host 0.0.0.0 --port 8432
curl http://127.0.0.1:8432/health
```

## 5. Docker

```bash
docker build -t simulforge .
docker run -p 8432:8432 simulforge
```
