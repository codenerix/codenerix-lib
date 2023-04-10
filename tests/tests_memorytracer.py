from codenerix_lib.memorytracer import MemoryTracer


def test_memorytracer():
    mt = MemoryTracer()
    mt.memtracer_clean()
    data = mt.memtracer_top(onscreen=False)
    config = data["config"]
    top = data["top"]

    assert config == {
        "key_type": "lineno",
        "limit": 10,
        "percents": (50, 10),
    }

    assert data["other"] is None or isinstance(data["other"], int)
    assert data["otherkb"] is None or isinstance(data["otherkb"], float)
    assert isinstance(data["total"], int)
    assert isinstance(data["totalkb"], float)

    idx = 1
    for line in top:
        assert line["index"] == idx
        idx += 1
        assert isinstance(line["filename"], str) and len(line["filename"]) > 0
        assert isinstance(line["linenumber"], int)
        assert isinstance(line["size"], int)
        assert isinstance(line["sizekb"], float)
        break
        print(line)
