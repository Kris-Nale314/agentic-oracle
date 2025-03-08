# tools/fmp_tool.py
import os
import requests
import time
import logging
from typing import Dict, Any, List, Optional
import json

# Configure logger
logger = logging.getLogger("agentic_oracle.fmp")

class FMPTool:
    """Tool to access Financial Modeling Prep (FMP) API data with rate limiting."""

    def __init__(self, api_key: Optional[str] = None, max_rpm: int = 10):
        """
        Initialize the FMP Tool with API key and rate limiting.
        
        Args:
            api_key: Optional API key (defaults to FMP_API_KEY environment variable)
            max_rpm: Maximum requests per minute to respect API rate limits
        """
        self.api_key = api_key or os.environ.get("FMP_API_KEY")
        if not self.api_key:
            raise ValueError("FMP API key is required")

        self.base_url = "https://financialmodelingprep.com/api/v3"
        self.max_rpm = max_rpm
        self.request_times = []  # For tracking request timestamps
        
        logger.info(f"FMPTool initialized with max_rpm={max_rpm}")

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a request to the FMP API with rate limiting.
        
        Args:
            endpoint: API endpoint to call
            params: Optional parameters for the request
            
        Returns:
            JSON response from the API or error dictionary
        """
        # Initialize params if None
        if params is None:
            params = {}
        
        # Add API key to params
        params["apikey"] = self.api_key
        
        # Implement rate limiting
        current_time = time.time()
        
        # Remove timestamps older than 60 seconds
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # If we've hit the rate limit, wait
        if len(self.request_times) >= self.max_rpm:
            wait_time = 60 - (current_time - self.request_times[0])
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
                # Update current time after waiting
                current_time = time.time()
                # Clean up request times again
                self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        # Log the request for debugging
        logger.debug(f"Making request to FMP API: {endpoint} with params: {params}")
        
        try:
            # Add this request to tracking
            self.request_times.append(current_time)
            
            # Make the API request
            response = requests.get(
                f"{self.base_url}/{endpoint}", 
                params=params, 
                timeout=10
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            
            # Check for FMP-specific error messages within the JSON
            if isinstance(data, dict) and (data.get("Error Message") or data.get("error")):
                error_msg = data.get("Error Message") or data.get("error")
                logger.error(f"FMP API returned error: {error_msg}")
                return {"error": f"FMP API error: {error_msg}"}
            
            # Check for empty response
            if not data:
                logger.warning(f"FMP API returned empty response for {endpoint}")
                return {"error": f"Empty response from FMP API for {endpoint}"}
            
            logger.debug(f"FMP API request successful")
            return data
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except requests.exceptions.Timeout:
            error_msg = f"Request to {endpoint} timed out after 10 seconds"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except json.JSONDecodeError:
            error_msg = f"Invalid JSON response from FMP API"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.exception(error_msg)  # Log full stack trace
            return {"error": error_msg}

    def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        """
        Get company profile information.
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Company profile data including industry, description, etc.
        """
        # Validate and normalize ticker
        if not ticker or not isinstance(ticker, str):
            logger.warning(f"Invalid ticker provided: {ticker}")
            return {
                "error": "Invalid ticker symbol",
                "name": "Unknown",
                "industry": "Unknown",
                "sector": "Unknown",
                "description": "Please provide a valid ticker symbol (e.g., AAPL, MSFT)"
            }
        
        # Clean and normalize ticker
        ticker = ticker.strip().upper()
        if not ticker:
            return {
                "error": "Empty ticker symbol",
                "name": "Unknown",
                "description": "Please provide a valid ticker symbol"
            }
        
        # Make API request
        logger.info(f"Fetching company profile for {ticker}")
        data = self._make_request(f"profile/{ticker}")
        
        # Check for API errors
        if isinstance(data, dict) and "error" in data:
            logger.warning(f"Error fetching profile for {ticker}: {data['error']}")
            return {
                "error": data["error"],
                "name": f"{ticker}",
                "industry": "Unknown",
                "sector": "Unknown",
                "description": f"Could not retrieve company profile. {data['error']}"
            }
        
        # Process successful response
        if isinstance(data, list) and len(data) > 0:
            profile = data[0]
            result = {
                "name": profile.get("companyName", ticker),
                "industry": profile.get("industry", "Unknown"),
                "sector": profile.get("sector", "Unknown"),
                "description": profile.get("description", "No description available"),
                "ceo": profile.get("ceo", "Unknown"),
                "website": profile.get("website", "Unknown"),
                "employees": profile.get("fullTimeEmployees", "Unknown"),
                "exchange": profile.get("exchange", "Unknown"),
                "marketCap": profile.get("mktCap", "Unknown"),
                "symbol": ticker
            }
            logger.info(f"Successfully retrieved profile for {ticker}")
            return result
        
        # Handle empty or unexpected response format
        logger.warning(f"No profile data found for {ticker}")
        return {
            "error": "No company profile found",
            "name": ticker,
            "industry": "Unknown",
            "sector": "Unknown",
            "description": f"No profile data was found for {ticker}. This might be an invalid ticker symbol or the company is not covered by the data provider."
        }

    def get_stock_quote(self, ticker: str) -> Dict[str, Any]:
        """
        Get current stock price and related information.
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Current stock quote data including price, change, volume, etc.
        """
        # Validate ticker
        if not ticker or not isinstance(ticker, str):
            return {"error": "Invalid ticker symbol"}
        
        ticker = ticker.strip().upper()
        
        # Make API request
        logger.info(f"Fetching stock quote for {ticker}")
        data = self._make_request(f"quote/{ticker}")
        
        # Check for API errors
        if isinstance(data, dict) and "error" in data:
            logger.warning(f"Error fetching quote for {ticker}: {data['error']}")
            return {"error": data["error"]}
        
        # Process successful response
        if isinstance(data, list) and len(data) > 0:
            quote = data[0]
            result = {
                "price": quote.get("price"),
                "change": quote.get("change"),
                "percentChange": quote.get("changesPercentage"),
                "dayLow": quote.get("dayLow"),
                "dayHigh": quote.get("dayHigh"),
                "yearLow": quote.get("yearLow"),
                "yearHigh": quote.get("yearHigh"),
                "marketCap": quote.get("marketCap"),
                "volume": quote.get("volume"),
                "avgVolume": quote.get("avgVolume"),
                "pe": quote.get("pe"),
                "eps": quote.get("eps"),
                "symbol": ticker
            }
            logger.info(f"Successfully retrieved quote for {ticker}")
            return result
        
        # Handle empty or unexpected response format
        logger.warning(f"No quote data found for {ticker}")
        return {
            "error": "No stock quote found",
            "symbol": ticker
        }

    def get_key_financials(self, ticker: str) -> Dict[str, Any]:
        """
        Get key financial metrics for a company.
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Key financial metrics including profitability, valuation, health, and growth
        """
        # Validate ticker
        if not ticker or not isinstance(ticker, str):
            return {"error": "Invalid ticker symbol"}
        
        ticker = ticker.strip().upper()
        
        # Make API requests for different financial endpoints
        logger.info(f"Fetching financial data for {ticker}")
        
        # Financial ratios
        ratios = self._make_request(f"ratios-ttm/{ticker}")
        if isinstance(ratios, dict) and "error" in ratios:
            logger.warning(f"Error fetching ratios for {ticker}: {ratios['error']}")
        
        # Income statement
        income = self._make_request(f"income-statement/{ticker}", {"limit": 1})
        if isinstance(income, dict) and "error" in income:
            logger.warning(f"Error fetching income statement for {ticker}: {income['error']}")
        
        # Balance sheet
        balance = self._make_request(f"balance-sheet-statement/{ticker}", {"limit": 1})
        if isinstance(balance, dict) and "error" in balance:
            logger.warning(f"Error fetching balance sheet for {ticker}: {balance['error']}")
        
        # Cash flow statement
        cash_flow = self._make_request(f"cash-flow-statement/{ticker}", {"limit": 1})
        if isinstance(cash_flow, dict) and "error" in cash_flow:
            logger.warning(f"Error fetching cash flow for {ticker}: {cash_flow['error']}")
        
        # Check if all requests failed
        if (isinstance(ratios, dict) and "error" in ratios and
            isinstance(income, dict) and "error" in income and
            isinstance(balance, dict) and "error" in balance and
            isinstance(cash_flow, dict) and "error" in cash_flow):
            logger.error(f"All financial data requests failed for {ticker}")
            return {"error": "Could not retrieve financial data"}
        
        # Extract financial data
        financial_data = {
            "ratios": ratios[0] if isinstance(ratios, list) and len(ratios) > 0 else {},
            "income": income[0] if isinstance(income, list) and len(income) > 0 else {},
            "balance": balance[0] if isinstance(balance, list) and len(balance) > 0 else {},
            "cashFlow": cash_flow[0] if isinstance(cash_flow, list) and len(cash_flow) > 0 else {},
        }
        
        # Construct result with data found
        result = {
            "profitability": {
                "grossMargin": financial_data["ratios"].get("grossProfitMarginTTM"),
                "operatingMargin": financial_data["ratios"].get("operatingProfitMarginTTM"),
                "netMargin": financial_data["ratios"].get("netProfitMarginTTM"),
                "roe": financial_data["ratios"].get("returnOnEquityTTM"),
                "roa": financial_data["ratios"].get("returnOnAssetsTTM"),
            },
            "valuation": {
                "pe": financial_data["ratios"].get("priceEarningsRatioTTM"),
                "pb": financial_data["ratios"].get("priceToBookRatioTTM"),
                "ps": financial_data["ratios"].get("priceToSalesRatioTTM"),
                "pfcf": financial_data["ratios"].get("priceToFreeCashFlowsRatioTTM"),
            },
            "health": {
                "currentRatio": financial_data["ratios"].get("currentRatioTTM"),
                "debtToEquity": financial_data["ratios"].get("debtEquityRatioTTM"),
                "interestCoverage": financial_data["ratios"].get("interestCoverageTTM"),
            },
            "growth": {
                "revenue": financial_data["income"].get("revenue"),
                "netIncome": financial_data["income"].get("netIncome"),
                "totalAssets": financial_data["balance"].get("totalAssets"),
                "totalDebt": financial_data["balance"].get("totalDebt"),
                "freeCashFlow": financial_data["cashFlow"].get("freeCashFlow"),
            },
            "symbol": ticker
        }
        
        logger.info(f"Successfully retrieved financial data for {ticker}")
        return result

    def get_news_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Get recent news articles for a company.
        
        Args:
            ticker: Company stock ticker symbol
            
        Returns:
            Recent news articles and metadata
        """
        # Validate ticker
        if not ticker or not isinstance(ticker, str):
            return {"error": "Invalid ticker symbol", "articles": []}
        
        ticker = ticker.strip().upper()
        
        # Make API request
        logger.info(f"Fetching news for {ticker}")
        data = self._make_request(f"stock_news", {"tickers": ticker, "limit": 10})
        
        # Check for API errors
        if isinstance(data, dict) and "error" in data:
            logger.warning(f"Error fetching news for {ticker}: {data['error']}")
            return {"error": data["error"], "articles": [], "symbol": ticker}
        
        # Process successful response
        if isinstance(data, list):
            articles = []
            for article in data:
                articles.append({
                    "title": article.get("title", "No title"),
                    "date": article.get("publishedDate", "Unknown date"),
                    "source": article.get("site", "Unknown source"),
                    "url": article.get("url", "#"),
                    "summary": article.get("text", "No summary available")
                })
            
            result = {
                "articles": articles,
                "count": len(articles),
                "symbol": ticker
            }
            
            logger.info(f"Successfully retrieved {len(articles)} news articles for {ticker}")
            return result
        
        # Handle empty or unexpected response format
        logger.warning(f"No news data found for {ticker}")
        return {
            "error": "No news found",
            "articles": [],
            "symbol": ticker
        }