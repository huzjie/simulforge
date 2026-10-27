# -*- coding: utf-8 -*-
"""Run standalone: python examples/05_http_client.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
from urllib.request import urlopen, Request


def post(url, obj):
    data = json.dumps(obj).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    base = "http://127.0.0.1:8432"
    print("health:", post(base + "/v1/interpret", {"audio_id": "http-demo"}) and
          json.loads(urlopen(base + "/health").read()))
    print("interpret:", post(base + "/v1/interpret",
                              {"audio_id": "http-demo", "speaker_id": "spk"}))


if __name__ == "__main__":
    main()
