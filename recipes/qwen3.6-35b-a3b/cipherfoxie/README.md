# Qwen3.6-35B-A3B AutoRound int4-mixed + DFlash (vLLM)

Production daily-driver config from a single DGX Spark (GB10, 128 GB unified
memory). This exact setup has served as the resident coding/agent model behind
a self-hosted stack since 2026-06-11.

## Measured (same box, same ruler: prefill-separated 256-token decode, temperature 0, median of 3)

| build | decode | deterministic coding gate | vision |
|---|---|---|---|
| **AutoRound int4-mixed + DFlash k=3 (this recipe)** | **69.2 tok/s** | 18/18 | tower present, works |
| 4.75-bit compressed-tensors + DFlash k=3 | 61.4 tok/s | 18/18 | dropped in build |
| FP8 | not viable on GB10 | 0/7 (reasoning loops) | n/a |

Cross-checked against vLLM's own TPOT metric (agreement within a fraction of
a tok/s, after warmup; note that DFlash needs a real request window to warm
up, cold readings undersell it by ~35%).

## Notes

- `gpu_memory_utilization` defaults to **0.5** so the desktop and co-resident
  services survive on unified memory. Raise it on a dedicated box.
- Defaults to text-only (`--language-model-only`), which is the measured
  config. The AutoRound build ships the full vision tower; launch with
  `-o extra_flags=` (empty) to load it and accept images. Verified on GB10.
- The coding gate is deterministic (typecheck + actual rename verification,
  no LLM judging): [agent-bench](https://github.com/cipherfoxie/agent-bench).
- Spark Arena leaderboard numbers for this model class come from the Arena's
  own harness (short generation bursts) and land above the conservative
  prefill-separated figure quoted here. Both are honest; they are different
  rulers, and only same-ruler numbers should ever be compared. Background:
  https://sovgrid.org/blog/catching-your-benchmark-lying-three-measurement-traps/

Full method, raw numbers, and the three-quant comparison:
https://sovgrid.org/blog/qwen3-35b-quant-comparison-autoround-prismaquant-fp8/
