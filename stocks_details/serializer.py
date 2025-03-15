"""Serializer for Stock model."""

from rest_framework import serializers

from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model."""

    class Meta:
        """Meta class for serializer."""

        model = Stock
        fields = (
            "__all__"  # You can specify fields like ['id', 'name', 'price']
        )
