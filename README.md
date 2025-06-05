# Financial P/E Analysis Tool

This repository provides simple utilities for evaluating whether a stock is potentially undervalued based on its price-to-earnings (P/E) ratio.  Stock prices and earnings information are fetched from the Alpha Vantage public API.

## Overview

1. **Fetch market data** – Current closing prices and EPS data are retrieved for any ticker symbol.
2. **Calculate P/E ratios** – The price is divided by earnings per share.
3. **Flag undervalued stocks** – Tickers with a P/E ratio below a configurable threshold are highlighted.

## Setup

1. Install the required dependencies:
   ```bash
   pip install requests
   ```
2. Edit `config.json` and provide your Alpha Vantage API key and desired P/E threshold:
   ```json
   {
       "financial_api_key": "YOUR_FINANCIAL_API_KEY",
       "pe_threshold": 15
   }
   ```

## Usage

Run the CLI and supply one or more ticker symbols. You can also specify a custom threshold with `--threshold`.

```bash
python financial_cli.py AAPL MSFT --threshold 12
```

If no tickers are supplied on the command line, the tool will prompt for a comma-separated list.

The script prints the calculated P/E for each ticker and lists those below the threshold.

## License

This project is licensed under the MIT License.
