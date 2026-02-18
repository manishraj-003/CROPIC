from app.services.discrepancy import compute_discrepancy, should_flag


def test_discrepancy_threshold():
    delta = compute_discrepancy(0.8, 0.3)
    assert delta == 0.5
    assert should_flag(delta, 0.3)
    assert not should_flag(0.2, 0.3)
