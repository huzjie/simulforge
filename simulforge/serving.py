# -*- coding: utf-8 -*-
"""A dependency-free HTTP server exposing the interpretation engine.

Uses only the standard library (``http.server``) so the managed runtime stays
self-contained. Endpoints:

  * ``GET  /health``            -> {"status": "ok"}
  * ``GET  /v1/models``         -> model/declared info
  * ``POST /v1/interpret``      -> {"audio_id": ..., "speaker_id": ...}
  * ``POST /v1/interpret/direct`` -> direct S2S path

Start with ``python -m simulforge.serving`` or via the CLI ``simulforge serve``.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .engine import SimultaneousEngine


class _Handler(BaseHTTPRequestHandler):
    engine = None

    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok", "skill": self.engine.skill})
        elif self.path == "/v1/models":
            d = self.engine.cfg.declared
            self._send(200, {"project": d.project, "model": d.model,
                             "language_pair": d.language_pair,
                             "latency_seconds": d.latency_seconds,
                             "license": d.license})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except Exception:
            self._send(400, {"error": "invalid json"})
            return
        audio_id = body.get("audio_id", "default-audio")
        speaker_id = body.get("speaker_id")
        if self.path == "/v1/interpret/direct":
            result = self.engine.interpret(audio_id, speaker_id, direct=True)
        elif self.path == "/v1/interpret":
            result = self.engine.interpret(audio_id, speaker_id, direct=False)
        else:
            self._send(404, {"error": "not found"})
            return
        self._send(200, _summary(result))

    def log_message(self, *args):
        pass


def _summary(result):
    return {
        "audio_id": result["audio_id"],
        "speaker_id": result["speaker_id"],
        "policy": result["policy"],
        "source_len": result["source_len"],
        "target_len": result["target_len"],
        "bleu": round(result["bleu"], 4),
        "quality": round(result["quality"], 4),
        "similarity": round(result["similarity"], 4),
        "streamlaal_s": round(result["latency"]["streamlaal_s"], 3),
        "direct": result["direct"],
    }


def serve(host="127.0.0.1", port=8432, skill=0.5, cfg=None):
    engine = SimultaneousEngine(skill=skill, cfg=cfg)
    _Handler.engine = engine
    httpd = HTTPServer((host, port), _Handler)
    print("simulforge serving on http://%s:%d (skill=%.2f)" % (host, port, skill),
          flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8432)
    ap.add_argument("--skill", type=float, default=0.5)
    args = ap.parse_args()
    serve(args.host, args.port, args.skill)
