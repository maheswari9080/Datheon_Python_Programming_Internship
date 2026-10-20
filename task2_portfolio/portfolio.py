#!/usr/bin/env python3
"""Stock Portfolio Performance Tracker.

Datheon Python Internship - Task 02.
Executable via:
    python task2_portfolio/portfolio.py
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))

from task2_portfolio.constituents_loader import ConstituentValidator
from task2_portfolio.csv_exporter import DEFAULT_CSV_PATH, export_portfolio_to_csv
from task2_portfolio.portfolio_calculator import (
    DISCLAIMER,
    HoldingPosition,
    calculate_portfolio_summary,
)
from task2_portfolio.price_providers import PriceProvider

BANNER = r"""
================================================================================
                    STOCK PORTFOLIO PERFORMANCE TRACKER                         
                    Datheon Python Internship Project 02                        
================================================================================
"""


def format_table(positions: List[HoldingPosition]) -> str:
    """Format holdings in a neat ASCII table."""
    if not positions:
        return "No holdings currently recorded."

    headers = [
        "Ticker", "Company", "Qty", "Buy Price", "Cur Price", "Invested ($)", "Value ($)", "Gain/Loss ($)", "Gain/Loss (%)", "Price Source"
    ]
    rows = []
    for p in positions:
        cur_str = f"${p.current_price:.2f}" if p.current_price is not None else "N/A"
        mv_str = f"${p.market_value:.2f}" if p.market_value is not None else "N/A"
        gl_str = (
            f"{'+' if p.absolute_gain_loss >= 0 else ''}${p.absolute_gain_loss:.2f}"  # type: ignore
            if p.absolute_gain_loss is not None
            else "N/A"
        )
        glp_str = (
            f"{'+' if p.percentage_gain_loss >= 0 else ''}{p.percentage_gain_loss:.2f}%"  # type: ignore
            if p.percentage_gain_loss is not None
            else "N/A"
        )
        company_trunc = p.company[:18] + ".." if len(p.company) > 20 else p.company
        rows.append([
            p.ticker,
            company_trunc,
            f"{p.quantity:.2f}",
            f"${p.buy_price:.2f}",
            cur_str,
            f"${p.invested_capital:.2f}",
            mv_str,
            gl_str,
            glp_str,
            p.price_source[:15],
        ])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    def format_row(cells: List[str]) -> str:
        return " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells))

    separator = "-+-".join("-" * w for w in col_widths)
    output_lines = [format_row(headers), separator]
    for row in rows:
        output_lines.append(format_row(row))

    return "\n".join(output_lines)


def render_summary(positions: List[HoldingPosition]) -> str:
    """Generate summary card with totals and partial-valuation warnings."""
    summary = calculate_portfolio_summary(positions)
    lines = [
        "=" * 60,
        "                 PORTFOLIO VALUATION SUMMARY                    ",
        "=" * 60,
        f"  Total Positions Tracked:      {summary.total_positions}",
        f"  Positions with Market Quotes: {summary.priced_positions}",
        f"  Positions Unpriced:           {summary.unpriced_positions}",
        f"  Total Capital Invested:       ${summary.total_invested:,.2f}",
    ]

    if summary.total_market_value is not None:
        lines.append(f"  Total Market Value:           ${summary.total_market_value:,.2f}")
        prefix = "+" if (summary.total_gain_loss or 0) >= 0 else ""
        lines.append(
            f"  Total Return (Gain/Loss):     {prefix}${summary.total_gain_loss:,.2f} "
            f"({prefix}{summary.total_gain_loss_percent:.2f}%)"
        )
    else:
        lines.append("  Total Market Value:           UNAVAILABLE (No holdings currently priced)")
        lines.append("  Total Return (Gain/Loss):     UNAVAILABLE")

    if not summary.is_complete_valuation and summary.unpriced_positions > 0:
        lines.append("\n  [!] NOTICE: Partial valuation only. Unpriced holdings are omitted from")
        lines.append("      market value totals to avoid misleading under-reporting.")

    lines.append("=" * 60)
    return "\n".join(lines)


def get_demo_positions(validator: ConstituentValidator, provider: PriceProvider) -> List[HoldingPosition]:
    """Pre-built sample portfolio for demonstration."""
    sample_data = [
        ("AAPL", 15.0, 185.50),
        ("MSFT", 8.0, 390.00),
        ("NVDA", 25.0, 115.00),
        ("AMZN", 12.0, 175.20),
        ("TSLA", 10.0, 240.00),
    ]
    positions = []
    for sym, qty, buy in sample_data:
        _, comp, _ = validator.lookup(sym)
        price, src = provider.get_sample_price(sym)
        positions.append(
            HoldingPosition(
                ticker=sym,
                company=comp,
                quantity=qty,
                buy_price=buy,
                current_price=price,
                price_source=src,
            )
        )
    return positions


def interactive_session() -> None:
    """Run interactive menu-driven terminal session."""
    validator = ConstituentValidator()
    provider = PriceProvider()
    positions: List[HoldingPosition] = []

    print(BANNER)
    print(f"Status: Constituents {validator.load_status}")
    print(f"\n> {DISCLAIMER}\n")

    while True:
        print("\n--- MENU ---")
        print("1. Add a stock position")
        print("2. View current portfolio & valuation")
        print("3. Fetch offline sample prices for all holdings")
        print("4. Update current price manually for a holding")
        print("5. Load sample demo portfolio (5 popular holdings)")
        print("6. Export portfolio summary to CSV")
        print("7. Clear all holdings")
        print("8. Exit")

        try:
            choice = input("\nSelect an option (1-8): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break

        if choice == "1":
            print("\n-- Add Stock Position --")
            ticker = input("Enter ticker symbol (e.g. AAPL, MSFT): ").strip().upper()
            if not ticker:
                print("Error: Ticker cannot be empty.")
                continue

            is_valid, company, sector = validator.lookup(ticker)
            if is_valid:
                print(f"Verified S&P 500 Constituent: {company} | Sector: {sector}")
            else:
                print(f"Warning: '{ticker}' was not found in S&P 500 constituents dataset.")
                comp_input = input("Enter company name manually (or press Enter to use ticker): ").strip()
                company = comp_input if comp_input else ticker

            try:
                qty_str = input("Enter share quantity (e.g. 10.5): ").strip()
                qty = float(qty_str)
                price_str = input("Enter purchase price per share (e.g. 182.50): ").strip()
                buy_price = float(price_str)
            except ValueError:
                print("Error: Quantity and purchase price must be valid positive numbers.")
                continue

            try:
                # Ask if user wants to quote a current price
                quote_choice = input("Enter current price if known (press Enter to look up in sample feed): ").strip()
                cur_price: Optional[float] = None
                p_source = "Unpriced"
                if quote_choice:
                    cur_price = float(quote_choice)
                    p_source = "User Entry"
                else:
                    sample_p, s_src = provider.get_sample_price(ticker)
                    if sample_p is not None:
                        cur_price = sample_p
                        p_source = s_src

                pos = HoldingPosition(
                    ticker=ticker,
                    company=company,
                    quantity=qty,
                    buy_price=buy_price,
                    current_price=cur_price,
                    price_source=p_source,
                )
                positions.append(pos)
                print(f"\n[+] Successfully added {qty} shares of {ticker} (${buy_price:.2f}/share).")
            except ValueError as ve:
                print(f"Error: {ve}")

        elif choice == "2":
            print("\n" + format_table(positions))
            print("\n" + render_summary(positions))

        elif choice == "3":
            print("\n-- Applying Offline Sample Quotes --")
            updated = 0
            for pos in positions:
                p, src = provider.get_sample_price(pos.ticker)
                if p is not None:
                    pos.current_price = p
                    pos.price_source = src
                    updated += 1
            print(f"Applied quotes to {updated} of {len(positions)} holdings.")
            print("\n" + format_table(positions))
            print("\n" + render_summary(positions))

        elif choice == "4":
            if not positions:
                print("No positions in portfolio.")
                continue
            t_search = input("Enter ticker to update: ").strip().upper()
            found = [p for p in positions if p.ticker == t_search]
            if not found:
                print(f"Holding with ticker '{t_search}' not found.")
                continue
            try:
                new_p = float(input(f"Enter new current price for {t_search}: ").strip())
                for pos in found:
                    pos.current_price = new_p
                    pos.price_source = "Manual Update"
                print(f"Updated current price for {t_search} to ${new_p:.2f}.")
            except ValueError:
                print("Invalid price entered.")

        elif choice == "5":
            positions = get_demo_positions(validator, provider)
            print(f"\n[+] Loaded {len(positions)} demo holdings with offline sample quotes.")
            print("\n" + format_table(positions))
            print("\n" + render_summary(positions))

        elif choice == "6":
            if not positions:
                print("Cannot export empty portfolio. Add positions first.")
                continue
            csv_path = export_portfolio_to_csv(positions, mode="snapshot")
            print(f"\n[+] Portfolio successfully exported to CSV: {csv_path.resolve()}")

        elif choice == "7":
            positions.clear()
            print("\n[+] Cleared all portfolio positions.")

        elif choice == "8":
            print("\nThank you for using the Stock Portfolio Performance Tracker. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose an option from 1 to 8.")


def main() -> None:
    """Entry point with CLI argument support for automation."""
    parser = argparse.ArgumentParser(
        description="Stock Portfolio Performance Tracker (Datheon Python Internship Task 2)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run non-interactive demo with sample portfolio and print report.",
    )
    parser.add_argument(
        "--export-csv",
        type=str,
        default=None,
        help="Export results directly to specified CSV path.",
    )
    args = parser.parse_args()

    if args.demo:
        validator = ConstituentValidator()
        provider = PriceProvider()
        positions = get_demo_positions(validator, provider)
        print(BANNER)
        print(f"> {DISCLAIMER}\n")
        print(format_table(positions))
        print("\n" + render_summary(positions))
        target_csv = Path(args.export_csv) if args.export_csv else DEFAULT_CSV_PATH
        out = export_portfolio_to_csv(positions, output_path=target_csv)
        print(f"\nSaved CSV to: {out}")
        return

    interactive_session()


if __name__ == "__main__":
    main()
