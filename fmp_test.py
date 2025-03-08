#fmp_test.py
"""
test_fmp_tool.py - Test script for Financial Modeling Prep (FMP) API tool

This script tests all methods of the FMPTool class to verify they're working correctly.
It prints out the results of each API call in a readable format.

Usage:
    python test_fmp_tool.py [ticker]

If no ticker is provided, it defaults to "AAPL".
"""

import os
import sys
import json
import logging
from dotenv import load_dotenv
from tools.fmp_tool import FMPTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("fmp_test")

def pretty_print(data, title=None):
    """Print dictionary data in a readable format"""
    if title:
        print(f"\n{'-' * 40}")
        print(f"{title}")
        print(f"{'-' * 40}")
    
    if isinstance(data, dict):
        if "error" in data:
            print(f"❌ ERROR: {data['error']}")
        else:
            # Print in a more readable format
            for key, value in data.items():
                if isinstance(value, dict):
                    print(f"\n{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                elif isinstance(value, list):
                    print(f"\n{key} ({len(value)} items):")
                    for i, item in enumerate(value[:3]):  # Show first 3 items
                        if isinstance(item, dict):
                            print(f"  Item {i+1}:")
                            for k, v in item.items():
                                # Truncate long text values
                                if isinstance(v, str) and len(v) > 100:
                                    v = v[:100] + "..."
                                print(f"    {k}: {v}")
                        else:
                            print(f"  Item {i+1}: {item}")
                    if len(value) > 3:
                        print(f"  ... and {len(value) - 3} more items")
                else:
                    print(f"{key}: {value}")
    else:
        print(data)

def save_to_file(data, filename):
    """Save data to a JSON file for further inspection"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Full data saved to {filename}")

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for FMP API key
    if not os.environ.get("FMP_API_KEY"):
        print("❌ Error: FMP_API_KEY environment variable not set")
        print("Please set it in your .env file or as an environment variable")
        sys.exit(1)
    
    # Get ticker from command line arguments or use default
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    ticker = ticker.upper()
    
    print(f"🔍 Testing FMP Tool with ticker: {ticker}")
    
    # Initialize FMP Tool
    fmp_tool = FMPTool(max_rpm=10)
    print(f"✅ FMP Tool initialized successfully")
    
    # Test company profile
    print("\n📊 Testing get_company_profile()...")
    profile_data = fmp_tool.get_company_profile(ticker)
    pretty_print(profile_data, "COMPANY PROFILE")
    save_to_file(profile_data, f"{ticker}_profile.json")
    
    # Test stock quote
    print("\n📈 Testing get_stock_quote()...")
    quote_data = fmp_tool.get_stock_quote(ticker)
    pretty_print(quote_data, "STOCK QUOTE")
    save_to_file(quote_data, f"{ticker}_quote.json")
    
    # Test key financials
    print("\n💰 Testing get_key_financials()...")
    financials_data = fmp_tool.get_key_financials(ticker)
    pretty_print(financials_data, "KEY FINANCIALS")
    save_to_file(financials_data, f"{ticker}_financials.json")
    
    # Test news sentiment
    print("\n📰 Testing get_news_sentiment()...")
    news_data = fmp_tool.get_news_sentiment(ticker)
    pretty_print(news_data, "NEWS DATA")
    save_to_file(news_data, f"{ticker}_news.json")
    
    print("\n✅ All tests completed!")
    print(f"Full data saved to {ticker}_*.json files for detailed inspection")

if __name__ == "__main__":
    main()