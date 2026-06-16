# North Mini Code 1.0 — FP8 & NVFP4 (vLLM, single-node DGX Spark)

Recipes for [Cohere's North Mini Code 1.0](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) — a 30B-total / 3B-active MoE agentic coding model (`Cohere2MoeForCausalLM`) — on a single DGX Spark (GB10).

Two variants:
- **`…-fp8-vllm`** — official FP8 checkpoint (`CohereLabs/North-Mini-Code-1.0-fp8`), ~28 GB.
- **`…-nvfp4-vllm`** — our NVFP4 (4-bit) quant ([`XanuNetworks/North-Mini-Code-1.0-NVFP4`](https://huggingface.co/XanuNetworks/North-Mini-Code-1.0-NVFP4)), ~17 GB.

Both use the pullable `ghcr.io/spark-arena/dgx-vllm-eugr-nightly:latest` image (self-consistent torch 2.11.0 + vLLM with `Cohere2MoeForCausalLM`). `cohere_melody` (which provides the `cohere_command4` tool + reasoning parsers) is installed at launch.

## Runtime / VRAM
- Runtime: vLLM, tensor-parallel 1 (single GB10), FP8 KV cache, 256K context.
- VRAM: FP8 ~28 GB weights, NVFP4 ~17 GB weights; `gpu_memory_utilization 0.7` (sized so the `spark-arena-v1` 100K-depth × 10-concurrency point runs without KV preemption).

## Benchmarks (DGX Spark GB10, `spark-arena-v1`)
Decode throughput (tok/s), concurrency 1 → 10:

| depth | FP8 | NVFP4 |
|------:|-----------|-----------|
| 0       | 33.4 → 107.2 | **56.7 → 177.9** |
| 32,768  | 31.1 → 72.4  | **48.5 → 103.4** |
| 100,000 | 28.6 → 46.6  | **40.0 → 57.0**  |

Prefill (depth 0): FP8 ~5,700 tok/s, NVFP4 ~9,400 tok/s. **NVFP4 is ~1.4–1.7× faster than FP8 across decode, prefill, and TTFT**, via FlashInfer-TRTLLM FP4 MoE on the GB10's FP4 tensor cores.

## Quality
NVFP4 matches FP8 on HumanEval pass@1 (90.2% each; bf16 90.9%) — no measurable quality loss from 4-bit.
