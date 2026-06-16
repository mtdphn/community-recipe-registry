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

Two standard metrics — they measure different things:
- **Decode** = token generation, one token per step, memory-bound → tens of tok/s on Spark-class bandwidth (~273 GB/s).
- **Prefill** = prompt processing, the whole prompt in parallel, compute-bound → ~100× decode. It equals `prompt_size ÷ TTFT`, so the prefill figures below are just the measured TTFT expressed as tok/s.

**Decode throughput** (tok/s) — *per-user at concurrency 1 → aggregate at concurrency 10*:

| depth | FP8 | NVFP4 |
|------:|-----------|-----------|
| 0       | 33.4/user → 107 agg | **56.7/user → 178 agg** |
| 32,768  | 31.1/user → 72 agg  | **48.5/user → 103 agg** |
| 100,000 | 28.6/user → 47 agg  | **40.0/user → 57 agg**  |

*(per-user rate falls as concurrency rises — e.g. FP8 ~13 tok/s/user at 10 concurrent.)*

**Prefill (prompt processing) @ depth 0:** FP8 ~5,700 tok/s, NVFP4 ~9,400 tok/s — i.e. TTFT of **362 ms / 221 ms** for a 2,048-token prompt.

**Net: NVFP4 ≈ 1.4–1.7× faster than FP8** across decode, prefill, and TTFT (FlashInfer-TRTLLM FP4 MoE on the GB10's FP4 tensor cores).

## Quality
NVFP4 matches FP8 on HumanEval pass@1 (90.2% each; bf16 90.9%) — no measurable quality loss from 4-bit.
