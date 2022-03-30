from rest_framework.routers import DefaultRouter

from . import viewsets

store_router = DefaultRouter()
store_router.register(
    'products',
    viewsets.ProductModelViewSet,
    basename='product')
