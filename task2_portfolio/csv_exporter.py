"""CSV persistence module for Task 2 Portfolio summaries."""

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from task2_portfolio.portfolio_calculator import HoldingPosition

DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "portfolio_summary.csv"

FIELDNAMES: List[str] = [
    "timestamp",
    "ticker",
    "company",
    "quantity",
    "buy_price",
    "current_price",
    "invested_value",
    "market_value",
    "gain_loss",
    "gain_loss_percent",
    "price_source",
]


def export_portfolio_to_csv(
    positions: List[HoldingPosition],
    output_path: Optional[Path] = None,
    mode: str = "snapshot",
) -> Path:
    """Export positions to CSV according to documented policy.

    Args:
        positions: List of HoldingPosition objects.
        output_path: Path to target CSV. Defaults to task2_portfolio/portfolio_summary.csv.
        mode: 'snapshot' (overwrites with current portfolio state) or
              'append' (preserves historical valuation runs).

    Returns:
        Path of written CSV file.
    """
    target = output_path or DEFAULT_CSV_PATH
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    write_header = True
    open_mode = "w"

    if mode == "append" and target.exists() and target.stat().st_size > 0:
        write_header = False
        open_mode = "a"

    with open(target, mode=open_mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES,
            quoting=csv.QUOTE_MINIMAL,
        )
        if write_header:
            writer.writeheader()

        for pos in positions:
            writer.writerow({
                "timestamp": now_iso,
                "ticker": pos.ticker,
                "company": pos.company,
                "quantity": f"{pos.quantity:.4f}".rstrip("0").rstrip("."),
                "buy_price": f"{pos.buy_price:.2f}",
                "current_price": (
                    f"{pos.current_price:.2f}"
                    if pos.current_price is not None
                    else "N/A"
                ),
                "invested_value": f"{pos.invested_capital:.2f}",
                "market_value": (
                    f"{pos.market_value:.2f}"
                    if pos.market_value is not None
                    else "N/A"
                ),
                "gain_loss": (
                    f"{pos.absolute_gain_loss:.2f}"
                    if pos.absolute_gain_loss is not None
                    else "N/A"
                ),
                "gain_loss_percent": (
                    f"{pos.percentage_gain_loss:.2f}%"
                    if pos.percentage_gain_loss is not None
                    else "N/A"
                ),
                "price_source": pos.price_source,
            })

    return target
