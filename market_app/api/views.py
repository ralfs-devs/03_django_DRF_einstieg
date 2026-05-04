from rest_framework import viewsets
from .serializers import MarketSerializer, SellerSerializer, SellerSerializer, ProductSerializer
from market_app.models import Market, Seller, Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class MarketViewSet(viewsets.ModelViewSet):
    """
    List all markets, or create a new market.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class SellerViewSet(viewsets.ModelViewSet):
    """
    List all sellers, or create a new seller.
    """
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
