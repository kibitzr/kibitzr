from kibitzr.transformer import transform_factory


def test_jq_sample():
    pipeline = transform_factory({'transform': [{'jq': '.a'}]})
    ok, content = pipeline(True, '{"a": 1, "b": 2}')
    assert ok is True
    assert content == "1"
