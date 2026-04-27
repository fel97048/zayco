from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, StorageLocation, Product, InventoryLot, InventoryTransaction, ShoppingListItem


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'default_storage_location', 'unit', 'deleted_at')
    search_fields = ('name', 'barcode')
    list_filter = ('category', 'default_storage_location')

@admin.register(InventoryLot)
class InventoryLotAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'storage_location', 'quantity', 'expiry_date', 'created_by', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('storage_location',)

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'transaction_type', 'quantity', 'user', 'created_at')
    search_fields = ('product_name', 'storage_location_name')
    list_filter = ('transaction_type',)

@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'unit', 'is_purchased', 'added_by', 'purchased_at')
    search_fields = ('product_name',)
    list_filter = ('is_purchased',)
