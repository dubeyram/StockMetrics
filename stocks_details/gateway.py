"""Gateway for fetching stock data from NSE API."""

from django.db.models import Q
from rest_framework.response import Response

from StockMetrics import config
from stocks_details.models import Stock


def serialize_stock_list(queryset):
    """Format the Given Queryset."""
    return {
        "symbols": [
            {
                "symbol_info": stock.get("name"),
                "symbol": stock.get("symbol").split(".")[0],
            }
            for stock in queryset
        ],
    }


@config.cache_result(timeout=config.EXPIRY_SECONDS)
def get_stocks_list(query):
    """Fetch stock data from NSE API."""
    if not query:
        return Response({"error": "Query parameter is missing"}, status=400)

    all_stocks = Stock.objects.filter(
        Q(name__icontains=query) | Q(symbol__icontains=query),
    ).values("name", "symbol")
    return serialize_stock_list(all_stocks)
