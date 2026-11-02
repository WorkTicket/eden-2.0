from cognition.memory.stream import MemoryStream
from engine.llm.client import MockLLM


def test_retrieval_prefers_relevant():
    s = MemoryStream(MockLLM())
    s.add(0, "observation", "A fruit tree, heavy with fruit, 2 steps east.", 3)
    s.add(1, "observation", "Water, 4 steps north.", 3)
    s.add(2, "observation", "Eva says: the river is cold.", 3)
    top = s.retrieve("where can I find fruit", now=3, k=1)
    assert "fruit" in top[0].text


def test_roundtrip():
    llm = MockLLM()
    s = MemoryStream(llm)
    s.add(0, "observation", "hello world", 5)
    s2 = MemoryStream.from_dict(llm, s.to_dict())
    assert s2.items[0].text == "hello world"
    assert s2.importance_since_reflection == 5


def test_reflection_counter_ignores_reflections():
    s = MemoryStream(MockLLM())
    s.add(0, "reflection", "insight", 7)
    assert s.importance_since_reflection == 0
