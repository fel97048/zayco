from django.contrib.auth import password_validation
from django.utils import timezone
from rest_framework import serializers
from .models import (
    User,
    Category,
    StorageLocation,
    Product,
    InventoryLot,
    InventoryTransaction,
    ShoppingListItem,
)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'date_joined')
        read_only_fields = ('id', 'date_joined')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('ユーザー名が既に使用されています')
        return value

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at')


class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ('id', 'name', 'description', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    default_storage_location_name = serializers.CharField(source='default_storage_location.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'default_storage_location',
            'default_storage_location_name',
            'barcode',
            'unit',
            'description',
            'deleted_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('deleted_at', 'created_at', 'updated_at')

    def create(self, validated_data):
        product = super().create(validated_data)
        InventoryLot.objects.create(
            product=product,
            storage_location=product.default_storage_location,
            quantity=0,
            expiry_date=None,
            created_by=self.context['request'].user,
            purchased_date=None,
        )
        return product


class InventoryLotSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    category_name = serializers.CharField(source='product.category.name', read_only=True)
    storage_location_name = serializers.CharField(source='storage_location.name', read_only=True)

    class Meta:
        model = InventoryLot
        fields = [
            'id',
            'product',
            'product_name',
            'category_name',
            'storage_location',
            'storage_location_name',
            'quantity',
            'expiry_date',
            'purchased_date',
            'created_by',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('数量は0以上で入力してください')
        return value


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = [
            'id',
            'lot',
            'product',
            'user',
            'product_name',
            'transaction_type',
            'quantity',
            'storage_location_name',
            'expiry_date',
            'created_at',
        ]
        read_only_fields = ('id', 'user', 'product_name', 'storage_location_name', 'created_at', 'product')


class ShoppingListItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ShoppingListItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'unit',
            'is_purchased',
            'purchased_at',
            'added_by',
            'created_at',
        ]
        read_only_fields = ('id', 'product_name', 'unit', 'purchased_at', 'added_by', 'created_at')

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('数量は0.1以上で入力してください')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        item = ShoppingListItem.objects.create(
            added_by=user,
            product=product,
            quantity=validated_data['quantity'],
            unit=product.unit,
            product_name=product.name,
        )
        return item
