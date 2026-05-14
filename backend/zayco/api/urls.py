from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    UserMeView,
    CategoryViewSet,
    StorageLocationViewSet,
    ProductViewSet,
    InventoryLotViewSet,
    PurchaseView,
    UseInventoryView,
    InventorySummaryView,
    InventoryHistoryView,
    ShoppingListItemViewSet,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('storage-locations', StorageLocationViewSet, basename='storage-locations')
router.register('products', ProductViewSet, basename='products')
router.register('inventory/lots', InventoryLotViewSet, basename='inventory-lots')
router.register('shopping-list', ShoppingListItemViewSet, basename='shopping-list')

urlpatterns = [
    path('users/register', RegisterView.as_view(), name='register'),
    path('users/login', LoginView.as_view(), name='login'),
    path('users/me', UserMeView.as_view(), name='user-me'),
    path('inventory/purchase', PurchaseView.as_view(), name='inventory-purchase'),
    path('inventory/lots/<int:pk>/use', UseInventoryView.as_view(), name='inventory-use'),
    path('inventory/summary', InventorySummaryView.as_view(), name='inventory-summary'),
    path('inventory/history', InventoryHistoryView.as_view(), name='inventory-history'),
    path('', include(router.urls)),
]
