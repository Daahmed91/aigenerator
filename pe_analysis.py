import requests
from init import load_config

CONFIG = load_config()
API_KEY = CONFIG.get("financial_api_key")
PE_THRESHOLD = CONFIG.get("pe_threshold", 15)

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def fetch_price(symbol):
    """Fetch the latest closing price for a ticker."""
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    resp = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
    data = resp.json()
    series = data.get("Time Series (Daily)")
    if not series:
        return None
    latest_day = next(iter(series.values()))
    try:
        return float(latest_day["4. close"])
    except (KeyError, ValueError, TypeError):
        return None


def fetch_eps(symbol):
    """Fetch EPS data for a ticker."""
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    resp = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
    data = resp.json()
    try:
        return float(data.get("EPS", 0))
    except (ValueError, TypeError):
        return None


def calculate_pe(symbol):
    """Calculate P/E ratio for a single ticker."""
    price = fetch_price(symbol)
    eps = fetch_eps(symbol)
    if price is None or eps in (None, 0):
        return None
    return price / eps


def analyze_tickers(tickers, threshold=None):
    """Analyze a list of tickers and flag those below the threshold."""
    results = []
    undervalued = []
    threshold = threshold if threshold is not None else PE_THRESHOLD

    for ticker in tickers:
        ticker = ticker.upper()
        pe = calculate_pe(ticker)
        results.append({"symbol": ticker, "pe": pe})
        if pe is not None and pe < threshold:
            undervalued.append(ticker)

    return results, undervalued
