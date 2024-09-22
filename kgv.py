import json
import os
import yfinance as yf
from datetime import datetime

def get_pe_ratio(ticker):
    """
    Fetches the current P/E ratio for a given Yahoo Finance ticker.
    """
    stock = yf.Ticker(ticker)
    pe_ratio = stock.info.get("trailingPE", None)  # Get the trailing P/E ratio
    
    if pe_ratio:
        return {datetime.now().strftime("%Y-%m-%d"): pe_ratio}
    else:
        print(f"Could not find P/E ratio for ticker: {ticker}")
        return {}

def update_pe_cache(isin, ticker, cache_file):
    """
    Updates the cache with new P/E ratio data for a given ISIN and ticker.
    """
    existing_data = {}
    # Load existing cache if available
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            existing_data = json.load(f)

    # Get the latest P/E ratio data
    new_data = get_pe_ratio(ticker)
    
    # Update the cache with new data
    if new_data:
        for date, pe_ratio in new_data.items():
            if date not in existing_data:
                existing_data[date] = pe_ratio
    
    # Save the updated data back to the cache file
    with open(cache_file, 'w') as f:
        json.dump(existing_data, f, indent=4)

def process_isins(input_file):
    """
    Processes a list of ISINs and updates the P/E ratio data for each.
    """
    with open(input_file, 'r') as f:
        isin_data = json.load(f)
    
    for entry in isin_data['shares']:
        isin = entry.get('isin')
        ticker = entry.get('ticker')
        
        if not isin or not ticker:
            print(f"Missing data for entry: {entry}")
            continue
        
        cache_file = f"{isin}_pe_cache.json"
        print(f"Processing ISIN: {isin}, Ticker: {ticker}")
        update_pe_cache(isin, ticker, cache_file)

if __name__ == "__main__":
    input_file = 'isins.json'  # Input file containing the list of ISINs and tickers
    process_isins(input_file)
 
