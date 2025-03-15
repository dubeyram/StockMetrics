"""Gateway for fetching stock data from NSE API."""

import requests
from rest_framework.response import Response

from StockMetrics import config


# Function to fetch stock data from NSE API
@config.cache_result(timeout=config.EXPIRY_SECONDS)
def get_stocks_list(query):
    """Fetch stock data from NSE API."""
    if not query:
        return Response({"error": "Query parameter is missing"}, status=400)

    url = f"{config.NSE_STOCK_SEARCH_URL}{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
    }
    try:
        response = requests.get(url, headers=headers, timeout=3)
        return response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)
