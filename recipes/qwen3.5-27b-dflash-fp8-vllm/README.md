# qwen3.5-27b-dflash-fp8-vllm

Qwen3.5-27B-FP8 + DFlash speculative decoding (`z-lab/Qwen3.5-27B-DFlash`, `num_speculative_tokens=15`) on a single DGX Spark.

## Run

```bash
sparkrun arena benchmark @community/qwen3.5-27b-dflash-fp8-vllm
```

Server startup ~16 min. Full ladder (28 cells × n=3) ~10 hours.

## Results

`tg128` aggregate tok/s (sum across concurrent requests), n=3. Single DGX Spark GB10, 122 GiB unified memory.

| depth | c=1 | c=2 | c=5 | c=10 |
|---:|---:|---:|---:|---:|
| 0 | 28.30 | 42.11 | 70.57 | **89.00** |
| 4096 | 21.79 | 41.03 | 60.32 | 31.81 |
| 8192 | 21.19 | 39.19 | 28.27 | 13.73 |
| 16384 | 21.13 | 32.44 | 19.69 | 7.26 |
| 32768 | 19.70 | 24.53 | 7.06 | 3.34 |
| 65535 | 10.25 | 17.77 | 2.19 | 1.50 |
| 100000 | 9.40 | 13.97 | 1.15 | 0.93 |

## Pitfalls

- Read `tg_throughput.mean` from result JSONs — not `peak_throughput`.
- Depth labels are GPT-2 tokens (llama-benchy fallback when served-model-name isn't an HF id). Output throughput is in true Qwen tokens.

## Author

[@banana_baeee](https://twitter.com/banana_baeee)
