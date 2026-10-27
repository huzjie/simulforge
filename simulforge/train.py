# -*- coding: utf-8 -*-
"""Training loop for the mock backends (geometric skill climb).

The signal is monotonically increasing by construction (``skill += lr * (1 -
skill)``), which is the "monotone" training rule: every step moves closer to the
optimum, never oscillating. This mirrors how a real SimulMT model's policy and
models improve together under RL / distillation.
"""
from .engine import SimultaneousEngine


def train(engine=None, lr=0.3, max_steps=24, log_every=4):
    engine = engine or SimultaneousEngine(skill=0.5)
    trace = [engine.skill]
    for step in range(1, max_steps + 1):
        engine.train_step(lr)
        trace.append(engine.skill)
        if step % log_every == 0 or step == max_steps:
            print("[train] step=%2d skill=%.4f" % (step, engine.skill), flush=True)
    return engine, trace


if __name__ == "__main__":
    train()
