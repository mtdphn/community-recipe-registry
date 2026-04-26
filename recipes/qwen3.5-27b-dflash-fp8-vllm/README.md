# qwen3.5-27b-dflash-fp8-vllm

Qwen3.5-27B-FP8 with DFlash speculative decoding (drafter `z-lab/Qwen3.5-27B-DFlash`, `num_speculative_tokens=15`) on DGX Spark.

First spec-decode entry on the leaderboard.

## Result

6.14× speedup over the BF16 autoregressive baseline at depth=0, concurrency=1. Geomean 4.53× across 7 depths at c=1.

| depth | AR-BF16 tok/s | DFlash-FP8 tok/s | speedup |
|---:|---:|---:|---:|
| 0 | 4.38 | 26.91 | 6.14× |
| 4096 | 4.18 | 21.25 | 5.09× |
| 8192 | 4.14 | 22.62 | 5.46× |
| 16384 | 3.94 | 22.33 | 5.66× |
| 32768 | 4.23 | 19.57 | 4.63× |
| 65535 | 4.09 | 13.69 | 3.35× |
| 100000 | 3.96 | 10.37 | 2.62× |

Mean spec-decode acceptance length at d=0 is 4.90 tokens, so the theoretical ceiling is ~5.9×. Observed 6.14× sits within 4% of that ceiling — the small surplus comes from spec decode using the GPU more efficiently at c=1.

The full 28-cell ladder JSON is in `results/dflash-fp8.json` and `results/ar-bf16.json`. A fresh-server canary reproduction (5 trials per cell, 3 depths) is in `results/dflash-fp8-canary2.json` / `results/ar-bf16-canary2.json` — within ±10% of the canonical numbers.

## Run it

```bash
sparkrun arena benchmark @community/qwen3.5-27b-dflash-fp8-vllm
```

This will:
1. Pull the prebuilt nightly vLLM container.
2. Download `Qwen/Qwen3.5-27B-FP8` and `z-lab/Qwen3.5-27B-DFlash` (drafter).
3. Apply the llama-benchy patch via `post_commands` (you'll be asked to confirm — see `patches/llama-benchy-spec-decode-fix/`).
4. Launch vLLM, run the spark-arena-v1 ladder, upload the result.

Server startup takes ~7 minutes including flashinfer JIT autotune on Blackwell. The full bench is 4–6 hours.

## Required patch

`patches/llama-benchy-spec-decode-fix/` — without it, every spec-decode bench (DFlash, MTP, EAGLE, Medusa, ngram) is undercounted by ~5×. See its README for the gory details.

## Honest caveats

- **High concurrency + high depth: AR wins.** At `c≥5` with `depth≥32k`, DFlash drops below AR (e.g. 6.82 vs 13.32 tok/s at d=32k c=5). The KV cache holds 93k tokens; at c=10 × d=32k that's 320k tokens needed → cache thrashing, which hits the drafter harder than the target. Spec decode is the right tool for low-concurrency latency-critical work, not batched throughput at long context.
- **Tokenizer fallback for prompt sizing.** llama-benchy can't resolve `qwen3.5-27b` as an HF id from the served-model-name and falls back to GPT-2 tokens when constructing depth-N prompts. So "depth=4096" means 4096 GPT-2 tokens, which is roughly ±15% of the equivalent Qwen tokens. Speedup ratios are unaffected — both AR and DFlash see the same prompts. Output throughput is in true Qwen tokens (the patch reads vLLM's `completion_tokens`).
- **`peak_throughput` is misleading for spec decode.** It counts SSE chunks/sec, not tokens/sec. Use `tg_throughput` for the headline.

## Pinned versions

| Component | Version |
|---|---|
| vLLM | `0.19.2rc1.dev135+g342c58bc5.cu130` (commit `342c58bc5`) |
| flashinfer-python | `0.6.8.post1` |
| llama-benchy | `0.3.5` + the patch in `patches/` |

## Hardware

NVIDIA DGX Spark, GB10 Blackwell (sm_121a), 122 GiB unified memory, single GPU.

## Author

[@banana_baeee](https://twitter.com/banana_baeee)
