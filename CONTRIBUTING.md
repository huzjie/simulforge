# Contributing

Thanks for your interest in simulforge. This is a zero-dependency reference
implementation; contributions that keep it pure-Python are preferred.

## Setup

```bash
git clone https://github.com/huzjie/simulforge.git
cd simulforge
python -m unittest discover -s tests -t .
```

## Checklist

- No external runtime dependencies (standard library only).
- New modules stay deterministic (md5-seeded randomness, single oracle).
- Add a unit test under `tests/` for any new behavior.
- Keep benchmark metrics monotonic in `skill`; verify with `python -m simulforge.bench`.
