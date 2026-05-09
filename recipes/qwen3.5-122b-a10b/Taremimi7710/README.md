# Qwen3.5-122B-A10B — Hybrid INT4+FP8 + MTP-2 + FlashInfer

Qwen3.5-122B-A10B (122B params, 10B active MoE) running the **Full v2** optimization stack on a single DGX Spark GB10 (128 GiB unified memory).

## Optimizations

| Layer | Detail |
|---|---|
| Base weights | Intel AutoRound INT4 (`Intel/Qwen3.5-122B-A10B-int4-AutoRound`) |
| Dense layers | Hybrid: 144 dense layers promoted to FP8 (+9% speed) |
| Speculative decoding | MTP-2 (`num_speculative_tokens=2`) |
| LM Head | INT8 LM Head v2 patch |
| Attention | FlashInfer backend (required for MTP on SM121) |

Build pipeline: [albond/DGX_Spark_Qwen3.5-122B-A10B-AR-INT4](https://github.com/albond/DGX_Spark_Qwen3.5-122B-A10B-AR-INT4) V2.3

## Prerequisites

This recipe requires a **custom Docker image** (`vllm-qwen35-v2`) built via the `install.sh` script in the above repository. The standard `scitrera/dgx-spark-vllm` image will **not** work because it lacks the INT8 LM Head v2 patch and the hybrid checkpoint builder.

```bash
git clone https://github.com/albond/DGX_Spark_Qwen3.5-122B-A10B-AR-INT4.git
cd DGX_Spark_Qwen3.5-122B-A10B-AR-INT4
bash install.sh --no-launch   # ~1.5 hours (downloads 75GB model + builds Docker image)
```

## Run

```
sparkrun run qwen3.5-122b-a10b-int4fp8-mtp-vllm-Taremimi7710 --solo
```

Server startup ~13 min (weights load ~10 min + torch.compile + warmup ~3 min).

## Results

Benchmarked on DGX Spark GB10, `bench_qwen35.sh "v2-full"`, 2 runs:

| Test | Run 1 (tok/s) | Run 2 (tok/s) |
|---|---|---|
| Q&A (256 tok) | 49.5 | 49.0 |
| Code (512 tok) | 51.3 | **51.5** |
| JSON (1024 tok) | 49.8 | 49.3 |
| Math (64 tok) | 47.0 | 47.4 |
| LongCode (2048 tok) | 53.2 | **53.8** |

**Average ~50 tok/s, Peak 53.8 tok/s** — 2.1× faster than Ollama baseline (24 tok/s).

## Pitfalls

- `--attention-backend FLASHINFER` is **mandatory** for MTP on SM121. PyTorch backend will crash.
- Prefix caching (`--enable-prefix-caching`) is **incompatible** with MTP-2 speculative decoding.
- The model directory must contain `model_extra_tensors.safetensors` (MTP weights from Step 2).
- First launch takes ~13 min; subsequent launches with cached weights take ~5-7 min.

## Author

[@Taremimi7710](https://github.com/Taremimi7710)
