# llama-benchy SSE-chunk-counting fix

## What it does

Patches one spot in `llama_benchy/client.py` (~line 219) so that `result.total_tokens` comes from `usage.completion_tokens` (the authoritative count from vLLM) instead of counting streaming chunks.

## Why you need it

Stock llama-benchy (≤ 0.3.5) counts one token per SSE chunk that has `delta.content`. That's correct for plain autoregressive decoding (one chunk = one token), but spec decoding packs several accepted tokens into each chunk. So spec decode gets reported as ~5× slower than it actually is.

Same server, same run, just different counting:

| llama-benchy state | tg128 throughput |
|---|---|
| stock (chunk-counting) | 5.51 tok/s |
| with this patch | 24.55 tok/s |

The ~4.5× gap matches the mean acceptance length (~4.9).

## Why nobody else submitted spec decode yet

This is probably why. Filtering the live leaderboard's `tg128 (c1)` test for `mtp|spec|dflash|eagle|medusa|draft` returns zero entries, even though an official MTP recipe ships in the registry. People probably tried, saw spec decode looking slower than AR, and gave up.

## Idempotent

The patcher checks for a marker string before applying. Safe to run on every `sparkrun arena benchmark` — first time it patches, after that it just prints "already patched" and exits 0.

## Upstream

Submitted as eugr/llama-benchy PR #11. Once that lands and a release is cut, the `post_commands` line in the recipe can come out.
