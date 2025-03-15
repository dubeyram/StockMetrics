"""Module contains API views for handling stock-related operations."""

from functools import lru_cache

import requests
import yfinance as yf
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from StockMetrics import config

from .gateway import get_stocks_list
from .models import Stock
from .serializer import StockSerializer

logging = config.logging


# View to render the form for user input
class StockInputView(TemplateView):
    """A class that inherits from TemplateView and provides a form for user input."""

    template_name = "stocks_input.html"


class StockInfoView(APIView):
    """A class that inherits from View and provides stock information."""

    @config.cache_result(timeout=config.EXPIRY_SECONDS)
    def get_stock_info(self, nse_code):
        """Get stock information for a given NSE code.

        Returns a dictionary containing:
        - Stock name (company name).
        - Current market price (CMP).
        - All-time high (ATH).
        - Percentage difference between CMP and ATH.
        """
        try:
            # Get stock data and metadata
            stock = yf.Ticker(f"{nse_code}.NS")

            # Get stock info to retrieve the name
            stock_info = stock.info
            stock_name = stock_info.get(
                "longName",
                "N/A",
            )  # Fetches company name, or 'N/A' if not available

            # Download historical stock data
            stock_data = stock.history(period="max")

            # Check if the DataFrame is empty
            if stock_data.empty:
                return {
                    "nse_code": nse_code,
                    "stock_name": stock_name,
                    "error": "No data available for the specified NSE code.",
                }

            # Get current market price (CMP)
            current_price = stock_data["Close"].iloc[-1]

            # Get all-time high (ATH) price
            all_time_high = stock_data["High"].max()

            # Calculate percentage difference
            if all_time_high > 0:
                percentage_difference = (
                    (current_price - all_time_high) / all_time_high * 100
                )
            else:
                percentage_difference = 0

            # Return dictionary containing all the information
            return {
                "nse_code": nse_code,
                "stock_name": stock_name,
                "current_price": float(round(current_price, 2)),
                "all_time_high": float(round(all_time_high, 2)),
                "percentage_difference": str(round(percentage_difference, 2))
                + "%",
            }
        except ValueError:
            # Handle errors if NSE code is invalid or data cannot be downloaded
            return {
                "nse_code": nse_code,
                "error": "Invalid NSE code or data unavailable.",
            }

    def get(self, request):
        """Retrieve stock information for a list of NSE codes.

        Args:
            request (Request): The request object containing the NSE codes.

        Returns:
            Response: A list of stock information dictionaries.

        """
        nse_codes = request.GET.get("codes", "")
        stock_info = self.get_stock_info(nse_codes)

        return Response(stock_info)


class StocktListCreateAPIView(APIView):
    """A class that inherits from APIView and provides CRUD operations for stock data."""

    def get(self):
        """Retrieve all Stock objects.

        Returns:
            Response: A list of Stock objects.

        """
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new Stock object.

        Args:
            request (Request): The request object containing the Stock data to be created.

        Returns:
            Response: The created Stock data or an error message.

        """
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockDetailAPIView(APIView):
    """A class that inherits from APIView and provides CRUD operations for stock data."""

    def get_object(self, pk):
        """Get a Stock object with the given primary key.

        Args:
            pk (int): The primary key of the Stock object to be retrieved.

        Returns:
            Response: The Stock data or None if the Stock object does not exist.

        """
        try:
            return Stock.objects.get(pk=pk)
        except Stock.DoesNotExist:
            return None

    def get(self, pk):
        """Retrieve a Stock object with the given primary key.

        Args:
            pk (int): The primary key of the Stock object to be updated.

        Returns:
            Response: The Stock data or an error message.

        """
        stock = self.get_object(pk)
        if stock is None:
            return Response(
                {"error": "Stock not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update a Stock object with the given primary key.

        Args:
            request (Request): The request object containing the updated Stock data.
            pk (int): The primary key of the Stock object to be updated.

        Returns:
            Response: The updated Stock data or an error message.

        """
        stock = self.get_object(pk)
        if stock is None:
            return Response(
                {"error": "Stock not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        """Delete a Stock object with the given primary key.

        Args:
            pk (int): The primary key of the Stock object to be deleted.

        Returns:
            Response: A response object containing the deleted Stock object.

        """
        stock = self.get_object(pk)
        if stock is None:
            return Response(
                {"error": "Stock not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FetchNSEDataView(APIView):
    """Fetch stock data from NSE API."""

    def get(self, request):
        """Get stock data from the NSE API."""
        query = request.GET.get("q", "")
        if not query:
            return Response(
                {"error": "Query parameter is missing"},
                status=400,
            )

        try:
            response = get_stocks_list(query.lower())

            return Response(response)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=500)

@lru_cache(maxsize=5)
def get_config(requests):
    """Get the base URL for the GROWW API."""
    return JsonResponse({"APP_BASE_URL": settings.APP_BASE_URL})
