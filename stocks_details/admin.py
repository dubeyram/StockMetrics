"""Admin configuration for Stocks Details."""

from django.contrib import admin

from stocks_details.models import Industry, Sector, Stock

# Custom Configuration For Django Admin Panel
admin.site.site_header = "My Custom Admin Panel"
admin.site.site_title = "Admin | MySite"
admin.site.index_title = "Welcome to My Admin Dashboard"


# Register your models here.
class StockAdmin(admin.ModelAdmin):
    """Admin configuration for Stock model."""

    list_display = ("symbol", "name", "industry", "market_cap")
    list_editable = ("name",)


class IndustryAdmin(admin.ModelAdmin):
    """Admin configuration for Industry model."""

    list_display = ("name", "sector")
    list_editable = ("sector",)


class SectorAdmin(admin.ModelAdmin):
    """Admin configuration for Sector model."""

    list_display = ("name",)


admin.site.register(Stock, StockAdmin)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Sector, SectorAdmin)
