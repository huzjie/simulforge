# -*- coding: utf-8 -*-
"""Allow ``python -m simulforge`` to run the CLI."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
