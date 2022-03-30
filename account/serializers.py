from rest_framework import serializers
from .models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('deposit', )
        model = User


class BuyerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = ('username', 'password')
        model = User

    def create(self, validated_data):
        user = User.create_objects.create_buyer(**validated_data)
        return user


class SellerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        fields = ('username', 'password')
        model = User

    def create(self, validated_data):
        user = User.create_objects.create_seller(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', )
        model = User


class UserDepositSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('deposit', )
        model = User

    ACCEPTED_DEPOSIT_VALUE = [5, 10, 20, 50, 100]

    def validate_deposit(self, value):
        if value not in self.ACCEPTED_DEPOSIT_VALUE:
            raise serializers.ValidationError(f'deposit should be one of {self.ACCEPTED_DEPOSIT_VALUE}')
        return value

    def update(self, instance, validated_data):
        instance.deposit = instance.deposit + validated_data.get('deposit')
        instance.save()
        return instance
