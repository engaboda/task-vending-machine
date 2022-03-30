from rest_framework.routers import DefaultRouter

from .viewsets import UserModelViewSet, BuyerViewSet

account_router = DefaultRouter()
account_router.register('user', UserModelViewSet, basename='user')
account_router.register('buyer', BuyerViewSet, basename='buyer')
