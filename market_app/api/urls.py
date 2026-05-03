from django.urls import path
from .views import MarketDetailView, MarketView, SellerView, products_view, product_single_view, SellerDetailView

urlpatterns = [
    path('market/', MarketView.as_view()),
    path('market/<int:pk>/', MarketDetailView.as_view(), name='market-detail'),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view(), name='seller-detail'),
    path('product/', products_view),
    path('product/<int:pk>/', product_single_view, name='product-detail'),
]
