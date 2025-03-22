from django.db import models


class Sector(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        related_name="industries",
    )

    def __str__(self):
        return self.name


class Stock(models.Model):
    symbol = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    industry = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE,
        related_name="stocks",
    )
    market_cap = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    pe_ratio = models.FloatField(
        null=True,
        blank=True,
    )  # Price-to-Earnings ratio
    dividend_yield = models.FloatField(null=True, blank=True)  # %

    def __str__(self):
        return f"{self.symbol} - {self.name}"
