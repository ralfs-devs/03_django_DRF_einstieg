from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, status, viewsets
from .serializers import MarketSerializer, ProducthyperlinkedSerializer, SellerSerializer, ProductSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Seller, Product
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductViewSetOld(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MarketView(generics.ListCreateAPIView):
    """
    List all markets, or create a new market.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a market instance.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class SellerView(generics.ListCreateAPIView):
    """
    List all sellers, or create a new seller.
    """
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SellerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a seller instance.
    """
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
