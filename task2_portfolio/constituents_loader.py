"""S&P 500 constituents loader and lookup validator for Task 2 Portfolio."""

import csv
from pathlib import Path
from typing import Dict, Optional, Tuple

DEFAULT_CONSTITUENTS_PATH = Path(__file__).resolve().parent / "data" / "constituents.csv"

# Fallback dictionary of common tickers if CSV is missing
FALLBACK_CONSTITUENTS: Dict[str, Dict[str, str]] = {
    "AAPL": {"security": "Apple Inc.", "sector": "Information Technology"},
    "MSFT": {"security": "Microsoft Corp.", "sector": "Information Technology"},
    "GOOGL": {"security": "Alphabet Inc. (Class A)", "sector": "Communication Services"},
    "AMZN": {"security": "Amazon.com Inc.", "sector": "Consumer Discretionary"},
    "NVDA": {"security": "NVIDIA Corp.", "sector": "Information Technology"},
    "TSLA": {"security": "Tesla Inc.", "sector": "Consumer Discretionary"},
    "META": {"security": "Meta Platforms Inc.", "sector": "Communication Services"},
    "BRK.B": {"security": "Berkshire Hathaway", "sector": "Financials"},
    "JNJ": {"security": "Johnson & Johnson", "sector": "Health Care"},
    "JPM": {"security": "JPMorgan Chase & Co.", "sector": "Financials"},
}


class ConstituentValidator:
    """Validates ticker symbols and resolves company names from S&P 500 constituents."""

    def __init__(self, csv_path: Optional[Path] = None) -> None:
        self.csv_path = csv_path or DEFAULT_CONSTITUENTS_PATH
        self.constituents: Dict[str, Dict[str, str]] = {}
        self.load_status: str = "unloaded"
        self._load()

    def _load(self) -> None:
        if self.csv_path.exists() and self.csv_path.is_file():
            try:
                with open(self.csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        symbol = row.get("Symbol", "").strip().upper()
                        security = row.get("Security", "").strip()
                        sector = row.get("GICS Sector", "").strip()
                        if symbol:
                            self.constituents[symbol] = {
                                "security": security or symbol,
                                "sector": sector or "Unknown",
                            }
                if self.constituents:
                    self.load_status = f"loaded ({len(self.constituents)} constituents)"
                    return
            except Exception as e:
                self.load_status = f"error loading csv: {e}; using fallback"

        # Fallback
        self.constituents = dict(FALLBACK_CONSTITUENTS)
        self.load_status = "fallback (default tickers loaded)"

    def lookup(self, ticker: str) -> Tuple[bool, str, str]:
        """Lookup a ticker. Returns (is_valid, company_name, sector)."""
        symbol = ticker.strip().upper()
        if symbol in self.constituents:
            info = self.constituents[symbol]
            return True, info["security"], info["sector"]
        return False, symbol, "Unknown"

    def is_known(self, ticker: str) -> bool:
        return ticker.strip().upper() in self.constituents
