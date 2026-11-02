# ADR-0003: Single LLM interface and mock-first development

- **Status:** accepted
- **Date:** 2026-11-02

## Context
LLM calls cost money and are non-deterministic. AI workers need a fast, free, repeatable loop. Models and providers will change.

## Decision
All model access goes through the `LLM` protocol in `engine/llm/client.py` (`complete`, `embed`). `MockLLM` is deterministic and is the default in tests and `make run`. Providers are optional dependencies imported lazily.

## Consequences
+ Tests never need a network or key. Provider swaps are local changes.
- Mock behavior is not representative of real agents; live runs are required for quality judgments. (T-109 improves the mock.)

## Alternatives
Direct SDK calls in cognition (rejected: couples, untestable).
