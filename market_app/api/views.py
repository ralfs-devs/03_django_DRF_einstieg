from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from .serializers import MarketSerializer, ProducthyperlinkedSerializer, SellerSerializer, ProductSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Seller, Product
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView


class MarketView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all markets, or create a new market.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MarketDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Retrieve, update or delete a market instance.
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SellerView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    List all sellers, or create a new seller.
    """
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SellerDetailView(APIView):
    """
    Retrieve, update or delete a seller instance.
    """

    def get_object(self, pk):
        return get_object_or_404(Seller, pk=pk)

    def get(self, request, pk):
        sellers = Seller.objects.filter(pk=pk)
        serializer = SellerSerializer(
            sellers, many=True, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        seller = self.get_object(pk)
        serializer = SellerSerializer(
            seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        seller = self.get_object(pk)
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProducthyperlinkedSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Anzeigen von Produktdetails (GET) für einzelne Produkte
# Änderung von Produktdetails (PUT)
# Löschen von Produkten (DELETE)


@api_view(['GET', 'PUT', 'DELETE'])
def product_single_view(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=400)
