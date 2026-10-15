from app.services.portfolio_state import PortfolioState


def test_portfolio_state_tracks_positions():
    state = PortfolioState(cash=100000.0, equity=100000.0)
    state.add_position("AAPL", 10, 100.0)
    state.update_equity()
    assert state.positions["AAPL"].quantity == 10
    assert state.cash == 99000.0
    assert state.equity > 0


def test_portfolio_state_can_liquidate_position():
    state = PortfolioState(cash=100000.0, equity=100000.0)
    state.add_position("MSFT", 5, 200.0)
    state.liquidate_position("MSFT", 210.0)
    assert "MSFT" not in state.positions
    assert state.cash > 99000.0
