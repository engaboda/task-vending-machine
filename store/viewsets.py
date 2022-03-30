from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import (
    ProductCreateSerializer, ProductListSerializer, ProductRetrieveSerializer, ProductUpdateSerializer
)
from .permissions import IsOwnerOrShowToAny


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrShowToAny)

    def get_serializer_class(self):
        if self.action == 'update':
            return ProductUpdateSerializer
        if self.action == 'create':
            return ProductCreateSerializer
        if self.action == 'list':
            return ProductListSerializer
        return ProductRetrieveSerializer


class BuyProductViewSet():
    pass
