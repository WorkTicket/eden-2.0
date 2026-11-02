# ADR-0004: Embeddings (PLACEHOLDER — decision pending)

- **Status:** proposed
- **Date:** 2026-11-02

## Context
Memory retrieval needs semantic similarity. v0.1 uses a hashing bag-of-words embedding (`hash_embed`) which only matches shared words. Anthropic's API does not provide an embeddings endpoint, so a separate provider or local model is needed.

## Options
1. Local sentence-transformers model (free, offline, adds torch dependency)
2. Hosted embedding API (simple, cost + data leaves machine)
3. Keep hashing embeddings plus an LLM reranker over top-k (no new dependency, extra calls)

## Decision
Pending human answer to TASKS Q2. Until then, keep `hash_embed`. Any choice must keep `LLM.embed` as the single interface and keep the mock deterministic.
