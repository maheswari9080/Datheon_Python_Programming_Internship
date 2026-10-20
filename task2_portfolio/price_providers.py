"""Price provider interface supporting manual entry, sample feeds, and optional live quotes."""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

SAMPLE_PRICES_PATH = Path(__file__).resolve().parent / "sample_prices.json"


class PriceProvider:
    """Manages price retrieval across offline feeds, user inputs, and optional live APIs."""

    def __init__(self, sample_file: Optional[Path] = None) -> None:
        self.sample_file = sample_file or SAMPLE_PRICES_PATH
        self.sample_quotes: Dict[str, float] = {}
        self._load_sample_feed()

    def _load_sample_feed(self) -> None:
        if self.sample_file.exists() and self.sample_file.is_file():
            try:
                with open(self.sample_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.sample_quotes = {
                        k.upper(): float(v)
                        for k, v in data.get("quotes", {}).items()
                    }
            except Exception:
                self.sample_quotes = {}

    def get_sample_price(self, ticker: str) -> Tuple[Optional[float], str]:
        """Fetch price from local offline reference file."""
        symbol = ticker.strip().upper()
        if symbol in self.sample_quotes:
            return self.sample_quotes[symbol], "Offline Sample Feed"
        return None, "Unavailable"

    def get_live_price_yfinance(self, ticker: str) -> Tuple[Optional[float], str]:
        """Attempt to fetch live quote via optional yfinance package if installed."""
        symbol = ticker.strip().upper()
        try:
            import yfinance as yf  # type: ignore

            t = yf.Ticker(symbol)
            fast_info = getattr(t, "fast_info", None)
            if fast_info and hasattr(fast_info, "last_price"):
                price = float(fast_info.last_price)
                if price > 0:
                    return round(price, 2), "Live Market (yfinance)"
            # Fallback to history
            hist = t.history(period="1d")
            if not hist.empty and "Close" in hist:
                price = float(hist["Close"].iloc[-1])
                return round(price, 2), "Live Market (yfinance)"
        except ImportError:
            return None, "yfinance not installed"
        except Exception as e:
            return None, f"Live fetch error: {e}"

        return None, "Unavailable"
