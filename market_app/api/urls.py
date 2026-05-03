from django.db import router
from django.urls import path, include
from .views import MarketDetailView, MarketView, SellerView, ProductSerializer, SellerDetailView, ProductViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name='seller-detail')
]
