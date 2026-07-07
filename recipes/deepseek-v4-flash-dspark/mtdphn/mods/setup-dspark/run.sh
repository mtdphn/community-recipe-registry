#!/bin/bash
# setup-dspark — prepare runtime directories for DSpark NVFP4
#
# This mod runs as a pre_exec hook inside every container before the
# serve command starts. It ensures JIT caches and runtime directories
# are writable, preventing import-time failures in flashinfer and vLLM.
#
# Idempotent — safe to run on every container start.

set -e

HF_CACHE="${HF_CACHE:-/cache/huggingface}"

# flashinfer JIT compiler writes a log file at import time.
# If the directory tree doesn't exist, the import crashes with:
#   PermissionError: flashinfer_jit.log
mkdir -p "${HF_CACHE}/flashinfer/.cache/flashinfer/0.6.12/121a"

# vLLM model info cache — non-fatal error if missing but noisy
mkdir -p "${HF_CACHE}/vllm-cache/modelinfos"

echo "setup-dspark: runtime directories ready"
