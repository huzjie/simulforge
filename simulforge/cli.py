# -*- coding: utf-8 -*-
"""Command-line interface for simulforge."""
import argparse
import json
import sys

from .config import load_config
from .engine import SimultaneousEngine


def _cmd_interpret(args):
    engine = SimultaneousEngine(skill=args.skill, cfg=load_config(args.config))
    r = engine.interpret(args.audio_id, args.speaker_id, direct=args.direct)
    print(json.dumps(_summary(r), indent=2, ensure_ascii=False))


def _summary(r):
    return {
        "audio_id": r["audio_id"],
        "speaker_id": r["speaker_id"],
        "policy": r["policy"],
        "direct": r["direct"],
        "source_len": r["source_len"],
        "target_len": r["target_len"],
        "transcript_len": len(r["transcript"]) if r["transcript"] else None,
        "translation_len": len(r["translation"]),
        "bleu": round(r["bleu"], 4),
        "quality": round(r["quality"], 4),
        "similarity": round(r["similarity"], 4),
        "streamlaal_s": round(r["latency"]["streamlaal_s"], 3),
        "al_words": round(r["latency"]["al_words"], 3),
    }


def _cmd_doctor(args):
    engine = SimultaneousEngine(skill=args.skill, cfg=load_config(args.config))
    r = engine.doctor()
    print("[doctor] skill=%.2f policy=%s" % (engine.skill, r["policy"]))
    print("[doctor] source_len=%d target_len=%d" % (r["source_len"], r["target_len"]))
    print("[doctor] bleu=%.4f quality=%.4f similarity=%.4f" %
          (r["bleu"], r["quality"], r["similarity"]))
    print("[doctor] StreamLAAL=%.3fs AL=%.3f words" %
          (r["latency"]["streamlaal_s"], r["latency"]["al_words"]))
    print("[doctor] OK")


def _cmd_serve(args):
    from .serving import serve
    serve(args.host, args.port, args.skill, load_config(args.config))


def _cmd_train(args):
    engine = SimultaneousEngine(skill=0.5, cfg=load_config(args.config))
    print("[train] start skill=%.4f" % engine.skill)
    for _ in range(args.steps):
        engine.train_step(args.lr)
    print("[train] end   skill=%.4f" % engine.skill)


def _cmd_bench(args):
    from .bench import run_all
    run_all(skill_sweep=True, n_sentences=args.n)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="simulforge",
                                 description="Streaming speech-to-speech simultaneous interpretation engine")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--config", default=None, help="path to a YAML config")
    common.add_argument("--skill", type=float, default=0.5)
    sub = ap.add_subparsers(dest="command")

    p = sub.add_parser("interpret", parents=[common])
    p.add_argument("audio_id", nargs="?", default="sample-1")
    p.add_argument("--speaker-id", default=None)
    p.add_argument("--direct", action="store_true")

    sub.add_parser("doctor", parents=[common])

    p = sub.add_parser("serve", parents=[common])
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8432)

    p = sub.add_parser("train", parents=[common])
    p.add_argument("--steps", type=int, default=24)
    p.add_argument("--lr", type=float, default=0.3)

    p = sub.add_parser("bench", parents=[common])
    p.add_argument("-n", type=int, default=64)

    args = ap.parse_args(argv)
    if args.command == "interpret":
        _cmd_interpret(args)
    elif args.command == "doctor":
        _cmd_doctor(args)
    elif args.command == "serve":
        _cmd_serve(args)
    elif args.command == "train":
        _cmd_train(args)
    elif args.command == "bench":
        _cmd_bench(args)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
