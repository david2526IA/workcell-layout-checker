from workcell_layout_checker.checker import check_layout


def item(identifier, x, y, width=1, height=1):
    return {"id": identifier, "x": x, "y": y, "width": width, "height": height}


def test_separated_layout_passes() -> None:
    report = check_layout({"minimum_clearance": 0.5, "equipment": [item("robot", 0, 0), item("conveyor", 2, 0)], "restricted_zones": [item("walkway", 5, 0)]})
    assert report["valid"] is True


def test_overlapping_or_near_items_are_reported() -> None:
    report = check_layout({"minimum_clearance": 0.5, "equipment": [item("robot", 0, 0), item("conveyor", 1.2, 0)], "restricted_zones": [item("walkway", 0.2, 1.2)]})
    assert report["valid"] is False
    assert {finding["kind"] for finding in report["findings"]} == {"equipment_clearance", "restricted_zone_clearance"}


def test_invalid_dimensions_are_rejected() -> None:
    try:
        check_layout({"equipment": [item("robot", 0, 0, width=0)]})
    except ValueError as error:
        assert "positive" in str(error)
    else:
        raise AssertionError("expected validation error")
