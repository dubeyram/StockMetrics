"""stocks_details URL Configuration."""

from django.urls import path

from .views import (
    FetchNSEDataView,
    StockDetailAPIView,
    StockInfoView,
    StockInputView,
    StocktListCreateAPIView,
    get_config,
)

urlpatterns = [
    path("diff-ath-cmp", StockInfoView.as_view(), name="diff_ath_cmp"),
    path("stock-list", StocktListCreateAPIView.as_view(), name="list_stocks"),
    path(
        "stock-list/<int:pk>",
        StockDetailAPIView.as_view(),
        name="list_stocks",
    ),
    path("", StockInputView.as_view(), name="stocks_iput"),
    path("fetch_nse/", FetchNSEDataView.as_view(), name="fetch_nse"),
    path("api/config/", get_config, name="config"),
]
