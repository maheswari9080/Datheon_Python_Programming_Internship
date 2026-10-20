"""Financial calculation engine for Task 2 Stock Portfolio Tracker."""

from dataclasses import dataclass
from typing import List, Optional

DISCLAIMER: str = (
    "EDUCATIONAL DISCLAIMER: This stock portfolio tracker is for academic and educational "
    "purposes only. It does not constitute financial, investment, or trading advice. Past "
    "performance and sample price feeds do not guarantee future market results."
)


@dataclass
class HoldingPosition:
    """Represents a single stock holding position."""
    ticker: str
    company: str
    quantity: float
    buy_price: float
    current_price: Optional[float] = None
    price_source: str = "Unpriced"

    def __post_init__(self) -> None:
        self.ticker = self.ticker.strip().upper()
        if not self.ticker:
            raise ValueError("Ticker symbol cannot be empty.")
        if self.quantity <= 0:
            raise ValueError(f"Quantity must be positive (> 0), got: {self.quantity}")
        if self.buy_price <= 0:
            raise ValueError(f"Purchase price must be positive (> 0), got: {self.buy_price}")
        if self.current_price is not None and self.current_price < 0:
            raise ValueError(f"Current price cannot be negative, got: {self.current_price}")

    @property
    def invested_capital(self) -> float:
        """P * Q: Total initial capital invested in this position."""
        return round(self.buy_price * self.quantity, 2)

    @property
    def market_value(self) -> Optional[float]:
        """C * Q: Current market value if current price is available."""
        if self.current_price is None:
            return None
        return round(self.current_price * self.quantity, 2)

    @property
    def absolute_gain_loss(self) -> Optional[float]:
        """(C - P) * Q: Absolute dollar return on investment."""
        if self.current_price is None:
            return None
        return round((self.current_price - self.buy_price) * self.quantity, 2)

    @property
    def percentage_gain_loss(self) -> Optional[float]:
        """((C - P) / P) * 100: Percentage return on investment."""
        if self.current_price is None:
            return None
        return round(((self.current_price - self.buy_price) / self.buy_price) * 100, 2)


@dataclass
class PortfolioSummary:
    """Aggregated portfolio valuation and return metrics."""
    total_positions: int
    priced_positions: int
    unpriced_positions: int
    total_invested: float
    total_market_value: Optional[float]
    total_gain_loss: Optional[float]
    total_gain_loss_percent: Optional[float]
    is_complete_valuation: bool


def calculate_portfolio_summary(positions: List[HoldingPosition]) -> PortfolioSummary:
    """Aggregate individual positions into a comprehensive portfolio summary."""
    if not positions:
        return PortfolioSummary(
            total_positions=0,
            priced_positions=0,
            unpriced_positions=0,
            total_invested=0.0,
            total_market_value=0.0,
            total_gain_loss=0.0,
            total_gain_loss_percent=0.0,
            is_complete_valuation=True,
        )

    total_invested = round(sum(p.invested_capital for p in positions), 2)
    priced = [p for p in positions if p.current_price is not None]
    unpriced = [p for p in positions if p.current_price is None]

    is_complete = len(unpriced) == 0

    if not priced:
        # None of the holdings have current market quotes
        return PortfolioSummary(
            total_positions=len(positions),
            priced_positions=0,
            unpriced_positions=len(unpriced),
            total_invested=total_invested,
            total_market_value=None,
            total_gain_loss=None,
            total_gain_loss_percent=None,
            is_complete_valuation=False,
        )

    total_market_value = round(sum(p.market_value for p in priced), 2)  # type: ignore
    invested_in_priced = sum(p.invested_capital for p in priced)
    total_gain_loss = round(total_market_value - invested_in_priced, 2)
    total_percent = (
        round((total_gain_loss / invested_in_priced) * 100, 2)
        if invested_in_priced > 0
        else 0.0
    )

    return PortfolioSummary(
        total_positions=len(positions),
        priced_positions=len(priced),
        unpriced_positions=len(unpriced),
        total_invested=total_invested,
        total_market_value=total_market_value if is_complete else total_market_value,
        total_gain_loss=total_gain_loss if is_complete else total_gain_loss,
        total_gain_loss_percent=total_percent if is_complete else total_percent,
        is_complete_valuation=is_complete,
    )
