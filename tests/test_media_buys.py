from media_buys import filter_media_buys, resolve_status_filter


def test_default_list_mode_uses_active_status():
    assert resolve_status_filter(None, None) == ["active"]


def test_explicit_status_filter_is_preserved():
    assert resolve_status_filter(None, ["paused", "active"]) == ["paused", "active"]


def test_ids_mode_skips_implicit_default_status_filter():
    assert resolve_status_filter(["buy-1"], None) is None


def test_empty_status_filter_is_rejected():
    try:
        resolve_status_filter(None, [])
        raise AssertionError("Expected ValueError for an empty status_filter")
    except ValueError:
        pass


def test_filter_media_buys_applies_default_active_behavior():
    buys = [
        {"id": "buy-1", "status": "active", "indicator_type": "CTR"},
        {"id": "buy-2", "status": "paused", "indicator_type": "CTR"},
        {"id": "buy-3", "status": "active", "indicator_type": "CPA"},
    ]

    assert filter_media_buys(buys) == [
        {"id": "buy-1", "status": "active", "indicator_type": "CTR"},
        {"id": "buy-3", "status": "active", "indicator_type": "CPA"},
    ]


def test_id_filter_keeps_explicit_status_filter_behavior():
    buys = [
        {"id": "buy-1", "status": "active", "indicator_type": "CTR"},
        {"id": "buy-2", "status": "paused", "indicator_type": "CTR"},
    ]

    assert filter_media_buys(buys, media_buy_ids=["buy-2"], status_filter=["paused"]) == [
        {"id": "buy-2", "status": "paused", "indicator_type": "CTR"}
    ]
