from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Meta:
        db_table = 'users'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class StorageLocation(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'storage_locations'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    default_storage_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        related_name='products'
    )
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, db_index=True)
    unit = models.CharField(max_length=20, default='個')
    description = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['deleted_at']),
        ]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()


class InventoryLot(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='inventory_lots'
    )
    storage_location = models.ForeignKey(
        StorageLocation,
        on_delete=models.PROTECT,
        related_name='inventory_lots'
    )
    quantity = models.FloatField(default=0)
    expiry_date = models.DateField(blank=True, null=True, db_index=True)
    purchased_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inventory_lots'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_lots'
        indexes = [
            models.Index(fields=['product', 'storage_location', 'expiry_date']),
            models.Index(fields=['expiry_date']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}{self.product.unit}"


class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('購入', '購入'),
        ('使用', '使用'),
    ]

    lot = models.ForeignKey(
        InventoryLot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='transactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inventory_transactions'
    )
    product_name = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.FloatField()
    storage_location_name = models.CharField(max_length=50)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} {self.product_name} {self.quantity}"


class ShoppingListItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='shopping_list_items'
    )
    product_name = models.CharField(max_length=255)
    quantity = models.FloatField(default=1)
    unit = models.CharField(max_length=20, default='個')
    is_purchased = models.BooleanField(default=False)
    added_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='shopping_list_items'
    )
    purchased_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shopping_list_items'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.product_name = self.product.name
        self.unit = self.product.unit
        if self.is_purchased and self.purchased_at is None:
            self.purchased_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} ({self.quantity}{self.unit})"
