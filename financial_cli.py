import argparse
from pe_analysis import analyze_tickers, PE_THRESHOLD


def main():
    parser = argparse.ArgumentParser(description="Analyze P/E ratios for stock tickers")
    parser.add_argument("tickers", nargs="*", help="List of stock tickers")
    parser.add_argument("--threshold", type=float, default=None, help="Custom P/E threshold")
    args = parser.parse_args()

    if args.tickers:
        tickers = [t.strip().upper() for t in args.tickers]
    else:
        user_input = input("Enter comma-separated tickers: ")
        tickers = [t.strip().upper() for t in user_input.split(",") if t.strip()]

    results, undervalued = analyze_tickers(tickers, args.threshold)
    threshold = args.threshold if args.threshold is not None else PE_THRESHOLD

    for res in results:
        if res["pe"] is None:
            print(f"{res['symbol']}: P/E unavailable")
        else:
            print(f"{res['symbol']}: P/E = {res['pe']:.2f}")

    if undervalued:
        print(f"\nUndervalued stocks (P/E < {threshold}): {', '.join(undervalued)}")
    else:
        print("\nNo stocks found below the threshold.")


if __name__ == "__main__":
    main()
