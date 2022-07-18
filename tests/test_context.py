from src.context import ContextHandle, context


def test_context_manager():
    outer = ContextHandle(outer=True)
    with context(name_1="value_1") as handle:
        assert "outer" in dict(handle)
        assert "name_1" in dict(handle)
        assert "name_2" not in dict(handle)

        handle.add(name_2="value_2")
        assert "name_1" in dict(handle)
        assert "name_2" in dict(handle)

        handle.remove("name_1")
        assert "name_1" not in dict(handle)
        assert "name_2" in dict(handle)

    assert "name_1" not in dict(outer)
    assert "name_2" not in dict(outer)
