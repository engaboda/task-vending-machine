from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status
from .models import User
from .serializers import (
    UserUpdateSerializer, UserRetrieveSerializer, BuyerCreateSerializer, SellerCreateSerializer, UserDepositSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSeller, IsBuyer, IsAuthenticatedOrCreate
from rest_framework.response import Response
from rest_framework.decorators import action
from store.serializers import ProductsBuySerializer
from store.models import Product
from store.exceptions import ProductNumberIsLargerThanProductAvailable, ProductPriceIsLargerThanUserDeposit
from django.db.models import F


class UserModelViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAuthenticatedOrCreate, )

    def get_object(self):
        """
            here we are using logged in user instead of id in url (not secure)
        """
        return self.request.user

    @action(detail=False, methods=['get'], serializer_class=UserRetrieveSerializer, url_name='detail')
    def detail_user(self, request, *args, **kwargs):
        """
            detail for logged in user.
        """
        assert request.user.is_authenticated is True, (
            "User is not Authenticated."
        )
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], serializer_class=UserUpdateSerializer, url_name='update')
    def update_user(self, request, *args, **kwargs):
        """
            the name should be update but this coflict with drf name
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=['delete'], url_name='destroy')
    def delete(self, request, *args, **kwargs):
        """
            delete user account.
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_update(self, serializer):
        serializer.save()

    @action(methods=['post'], detail=False, serializer_class=BuyerCreateSerializer)
    def create_buyer(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'created'}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, serializer_class=SellerCreateSerializer)
    def create_seller(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'created'}, status=status.HTTP_201_CREATED)


class BuyerViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDepositSerializer
    permission_classes = (IsAuthenticated, IsBuyer)

    @action(methods=['put'], detail=False)
    def deposit(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def calculate_total_price_amount_is_less_than_amount_available(self, data):
        total_price = 0
        products_amount = 0
        for item in data['product_info']:
            product = Product.objects.get(id=item.get('productId'))
            total_price += product.cost * item.get('amount_of_product')
            self.is_amount_less_than_product_amount_available(product.amountAvailable, item.get('amount_of_product'))
            self.update_amount_available(product, item.get('amount_of_product'))
        return total_price, products_amount

    def is_total_price_less_user_deposit(self, total_price):
        if self.request.user.deposit >= total_price:
            return True
        raise ProductPriceIsLargerThanUserDeposit()

    def is_amount_less_than_product_amount_available(self, available_amount, product_amount):
        if available_amount >= product_amount:
            return product_amount
        raise ProductNumberIsLargerThanProductAvailable()

    def update_amount_available(self, product, product_amount):
        product.amountAvailable = F('amountAvailable') - product_amount
        product.save()
        return True

    @action(methods=['post'], detail=False, serializer_class=ProductsBuySerializer)
    def buy(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_price, products_amount = self.calculate_total_price_amount_is_less_than_amount_available(serializer.validated_data)
        self.is_total_price_less_user_deposit(total_price)

        request.user.deposit = F('deposit') - total_price
        request.user.save()

        return Response({"total_price": total_price, "product": str(Product.productName), 'available_deposit': str(request.user.deposit)})

    @action(methods=['post'], detail=False)
    def reset_deposit(self, request, *args, **kwargs):
        request.user.reset_deposit()
        return Response({'message': 'Deposit is Reseted'})
