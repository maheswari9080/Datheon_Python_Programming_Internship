"""Automated unittest suite for Task 2 Stock Portfolio Performance Tracker."""

import csv
import tempfile
import unittest
from pathlib import Path

from task2_portfolio.constituents_loader import ConstituentValidator
from task2_portfolio.csv_exporter import FIELDNAMES, export_portfolio_to_csv
from task2_portfolio.portfolio_calculator import (
    DISCLAIMER,
    HoldingPosition,
    calculate_portfolio_summary,
)
from task2_portfolio.price_providers import PriceProvider


class TestHoldingPositionCalculations(unittest.TestCase):
    """Verify single-position financial mathematical operations."""

    def test_profitable_position(self) -> None:
        pos = HoldingPosition(
            ticker="AAPL",
            company="Apple Inc.",
            quantity=10.0,
            buy_price=150.00,
            current_price=180.00,
            price_source="Test Feed",
        )
        self.assertEqual(pos.invested_capital, 1500.00)
        self.assertEqual(pos.market_value, 1800.00)
        self.assertEqual(pos.absolute_gain_loss, 300.00)
        self.assertEqual(pos.percentage_gain_loss, 20.00)

    def test_loss_making_position(self) -> None:
        pos = HoldingPosition(
            ticker="XYZ",
            company="Test Corp",
            quantity=5.0,
            buy_price=100.00,
            current_price=80.00,
        )
        self.assertEqual(pos.invested_capital, 500.00)
        self.assertEqual(pos.market_value, 400.00)
        self.assertEqual(pos.absolute_gain_loss, -100.00)
        self.assertEqual(pos.percentage_gain_loss, -20.00)

    def test_unpriced_position_returns_none(self) -> None:
        pos = HoldingPosition(
            ticker="ABC",
            company="Unquoted Inc",
            quantity=10.0,
            buy_price=50.00,
            current_price=None,
        )
        self.assertEqual(pos.invested_capital, 500.00)
        self.assertIsNone(pos.market_value)
        self.assertIsNone(pos.absolute_gain_loss)
        self.assertIsNone(pos.percentage_gain_loss)

    def test_invalid_negative_price_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            HoldingPosition("AAPL", "Apple", quantity=10, buy_price=-50.0)

    def test_invalid_zero_buy_price_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            HoldingPosition("AAPL", "Apple", quantity=10, buy_price=0.0)

    def test_invalid_zero_quantity_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            HoldingPosition("AAPL", "Apple", quantity=0, buy_price=100.0)

    def test_invalid_negative_quantity_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            HoldingPosition("AAPL", "Apple", quantity=-5, buy_price=100.0)


class TestPortfolioAggregator(unittest.TestCase):
    """Verify multi-holding portfolio summarization and partial valuation rules."""

    def test_complete_portfolio(self) -> None:
        p1 = HoldingPosition("AAPL", "Apple", quantity=10.0, buy_price=100.0, current_price=120.0)
        p2 = HoldingPosition("MSFT", "Microsoft", quantity=5.0, buy_price=200.0, current_price=250.0)

        summary = calculate_portfolio_summary([p1, p2])
        self.assertEqual(summary.total_positions, 2)
        self.assertEqual(summary.priced_positions, 2)
        self.assertEqual(summary.unpriced_positions, 0)
        self.assertEqual(summary.total_invested, 2000.00)
        self.assertEqual(summary.total_market_value, 2450.00)
        self.assertEqual(summary.total_gain_loss, 450.00)
        self.assertEqual(summary.total_gain_loss_percent, 22.50)
        self.assertTrue(summary.is_complete_valuation)

    def test_partial_portfolio_flags_incomplete(self) -> None:
        p1 = HoldingPosition("AAPL", "Apple", quantity=10.0, buy_price=100.0, current_price=120.0)
        p2 = HoldingPosition("UNK", "Unknown Co", quantity=5.0, buy_price=200.0, current_price=None)

        summary = calculate_portfolio_summary([p1, p2])
        self.assertEqual(summary.total_positions, 2)
        self.assertEqual(summary.priced_positions, 1)
        self.assertEqual(summary.unpriced_positions, 1)
        self.assertFalse(summary.is_complete_valuation)

    def test_empty_portfolio(self) -> None:
        summary = calculate_portfolio_summary([])
        self.assertEqual(summary.total_positions, 0)
        self.assertEqual(summary.total_invested, 0.0)
        self.assertEqual(summary.total_market_value, 0.0)


class TestConstituentsLoader(unittest.TestCase):
    """Verify S&P 500 constituents lookup and fallback."""

    def test_known_ticker_lookup(self) -> None:
        validator = ConstituentValidator()
        is_valid, company, sector = validator.lookup("AAPL")
        self.assertTrue(is_valid)
        self.assertIn("Apple", company)

    def test_unknown_ticker_lookup(self) -> None:
        validator = ConstituentValidator()
        is_valid, company, sector = validator.lookup("TOTALLYFAKE999")
        self.assertFalse(is_valid)
        self.assertEqual(company, "TOTALLYFAKE999")


class TestCSVExporter(unittest.TestCase):
    """Verify CSV file generation, fieldnames, and snapshot/append modes."""

    def test_export_creates_valid_csv(self) -> None:
        pos = HoldingPosition("AAPL", "Apple Inc.", 10.0, 150.0, 180.0, "Test Source")
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tf:
            tf_path = Path(tf.name)

        try:
            export_portfolio_to_csv([pos], output_path=tf_path, mode="snapshot")
            self.assertTrue(tf_path.exists())

            with open(tf_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.assertEqual(reader.fieldnames, FIELDNAMES)
                rows = list(reader)
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["ticker"], "AAPL")
                self.assertEqual(rows[0]["invested_value"], "1500.00")
                self.assertEqual(rows[0]["market_value"], "1800.00")
                self.assertEqual(rows[0]["gain_loss"], "300.00")
                self.assertEqual(rows[0]["price_source"], "Test Source")
        finally:
            tf_path.unlink(missing_ok=True)

    def test_educational_disclaimer_present(self) -> None:
        self.assertIn("EDUCATIONAL DISCLAIMER", DISCLAIMER)
        self.assertIn("not constitute financial", DISCLAIMER)


if __name__ == "__main__":
    unittest.main()
