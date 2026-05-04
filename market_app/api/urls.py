from django.db import router
from django.urls import path, include
from .views import ProductViewSet, MarketViewSet, SellerViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'product', ProductViewSet)
router.register(r'market', MarketViewSet)
router.register(r'seller', SellerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('market/', MarketView.as_view()),
    # path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    # path('seller/', SellerView.as_view()),
    # path('seller/<int:pk>/', SellerDetailView.as_view(), name='seller-detail')
]
