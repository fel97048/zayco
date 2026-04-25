# Django実装ガイド

## 改訂履歴

| 版 | 日付 | 変更内容 |
|---|------|---------|
| 1.0 | 2025-03-11 | 初版作成（FastAPIからDjangoへ変更） |

## 1. 概要

このドキュメントは、在庫管理システムをDjango + Django REST Frameworkで実装する際のガイドです。

### 1.1 技術スタック

- **Django**: 4.2
- **Django REST Framework**: 3.14
- **認証**: djangorestframework-simplejwt
- **CORS**: django-cors-headers
- **データベース**: SQLite（開発）/ PostgreSQL（本番推奨）

### 1.2 FastAPIからの主な変更点

| 項目 | FastAPI | Django |
|------|---------|--------|
| ORM | SQLAlchemy | Django ORM |
| スキーマ | Pydantic | DRF Serializers |
| ルーティング | @app.get() デコレータ | urls.py + ViewSet |
| バリデーション | Pydantic validators | DRF validators |
| マイグレーション | Alembic | Django migrations |
| 認証 | python-jose | djangorestframework-simplejwt |

## 2. プロジェクト構造

```
inventory_project/
├── manage.py
├── inventory_project/          # プロジェクト設定
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/                        # APIアプリケーション
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py              # Django models
    ├── serializers.py         # DRF serializers
    ├── views.py               # DRF views/viewsets
    ├── urls.py                # URLルーティング
    ├── permissions.py         # カスタムパーミッション
    └── migrations/
        └── __init__.py
```

## 3. requirements.txt

```txt
Django==4.2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
python-dotenv==1.0.0
```

## 4. settings.py 設定

### 4.1 基本設定

```python
# inventory_project/settings.py

import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Local
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inventory_project.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### 4.2 REST Framework設定

```python
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%SZ',
    'DATE_FORMAT': '%Y-%m-%d',
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 4.3 CORS設定

```python
# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True
```

## 5. Models（Django ORM）

### 5.1 models.py

```python
# api/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """ユーザー（Djangoのビルトインユーザーを拡張）"""
    # AbstractUserを使うことでusername, password, emailなどが自動的に含まれる
    # カスタムフィールドがあれば追加
    
    class Meta:
        db_table = 'users'

class Category(models.Model):
    """カテゴリ"""
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class StorageLocation(models.Model):
    """保管場所"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'storage_locations'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """商品マスタ"""
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
        """論理削除"""
        self.deleted_at = timezone.now()
        self.save()

class InventoryLot(models.Model):
    """在庫ロット"""
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
    """在庫取引履歴"""
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
    product_id = models.IntegerField(blank=True, null=True)  # 削除対策
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inventory_transactions'
    )
    product_name = models.CharField(max_length=255)  # 削除対策
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.FloatField()
    storage_location_name = models.CharField(max_length=50, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.product_name}: {self.quantity}"

class ShoppingListItem(models.Model):
    """買い物リスト"""
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shopping_list_items'
    )
    product_name = models.CharField(max_length=255)
    quantity = models.FloatField(default=1)
    unit = models.CharField(max_length=20, default='個')
    is_purchased = models.BooleanField(default=False, db_index=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='shopping_list_items'
    )
    purchased_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'shopping_list_items'
        ordering = ['is_purchased', '-created_at']
    
    def __str__(self):
        return f"{self.product_name}: {self.quantity}{self.unit}"
```

## 6. Serializers（DRF）

### 6.1 serializers.py

```python
# api/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Category, StorageLocation, Product,
    InventoryLot, InventoryTransaction, ShoppingListItem
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    default_storage_location = StorageLocationSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    default_storage_location_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_id',
            'default_storage_location', 'default_storage_location_id',
            'barcode', 'unit', 'description',
            'deleted_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'deleted_at', 'created_at', 'updated_at']

class InventoryLotSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    storage_location = StorageLocationSerializer(read_only=True)
    created_by_user = UserSerializer(read_only=True, source='created_by')
    
    class Meta:
        model = InventoryLot
        fields = [
            'id', 'product', 'storage_location', 'quantity',
            'expiry_date', 'purchased_date', 'created_by_user',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PurchaseSerializer(serializers.Serializer):
    """購入登録用"""
    product_id = serializers.IntegerField()
    quantity = serializers.FloatField(min_value=0.1)
    storage_location_id = serializers.IntegerField()
    expiry_date = serializers.DateField(required=False, allow_null=True)
    purchased_date = serializers.DateField(required=False, allow_null=True)

class UseInventorySerializer(serializers.Serializer):
    """使用登録用"""
    quantity = serializers.FloatField(min_value=0.1)

class InventoryTransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InventoryTransaction
        fields = [
            'id', 'product_id', 'product_name', 'user',
            'transaction_type', 'quantity', 'storage_location_name',
            'expiry_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class ShoppingListItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    added_by_user = UserSerializer(read_only=True, source='added_by')
    
    class Meta:
        model = ShoppingListItem
        fields = [
            'id', 'product', 'product_name', 'quantity', 'unit',
            'is_purchased', 'added_by_user', 'purchased_at', 'created_at'
        ]
        read_only_fields = ['id', 'purchased_at', 'created_at']
```

## 7. Views（DRF ViewSets）

### 7.1 views.py（抜粋）

```python
# api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Product, InventoryLot, Category, StorageLocation
from .serializers import (
    ProductSerializer, InventoryLotSerializer,
    PurchaseSerializer, UseInventorySerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        """論理削除"""
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        return Response(
            {'message': '商品を削除しました'},
            status=status.HTTP_200_OK
        )

class InventoryLotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryLot.objects.select_related(
        'product', 'storage_location', 'created_by'
    )
    serializer_class = InventoryLotSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def purchase(self, request):
        """購入登録"""
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        storage_location_id = serializer.validated_data['storage_location_id']
        expiry_date = serializer.validated_data.get('expiry_date')
        quantity = serializer.validated_data['quantity']
        
        # ロット検索
        lot, created = InventoryLot.objects.get_or_create(
            product=product,
            storage_location_id=storage_location_id,
            expiry_date=expiry_date,
            defaults={
                'quantity': 0,
                'created_by': request.user,
                'purchased_date': serializer.validated_data.get('purchased_date')
            }
        )
        
        # 在庫加算
        lot.quantity += quantity
        lot.save()
        
        # 履歴記録
        # ...
        
        return Response(
            InventoryLotSerializer(lot).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def use(self, request, pk=None):
        """使用登録"""
        lot = self.get_object()
        serializer = UseInventorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        if lot.quantity < quantity:
            return Response(
                {'detail': '在庫が不足しています'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lot.quantity -= quantity
        lot.save()
        
        # 履歴記録
        # ...
        
        return Response(
            InventoryLotSerializer(lot).data,
            status=status.HTTP_200_OK
        )
```

## 8. URLs

### 8.1 inventory_project/urls.py

```python
# inventory_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include('api.urls')),
]
```

### 8.2 api/urls.py

```python
# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'inventory/lots', views.InventoryLotViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'storage-locations', views.StorageLocationViewSet)
router.register(r'shopping-list', views.ShoppingListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', views.RegisterView.as_view(), name='register'),
    path('users/me/', views.CurrentUserView.as_view(), name='current_user'),
]
```

## 9. マイグレーション

### 9.1 初回マイグレーション

```bash
# マイグレーションファイル作成
python manage.py makemigrations

# データベースに適用
python manage.py migrate
```

### 9.2 カスタムUserモデルの設定

```python
# settings.py
AUTH_USER_MODEL = 'api.User'
```

## 10. 初期データ投入

### 10.1 management command作成

```python
# api/management/commands/init_data.py

from django.core.management.base import BaseCommand
from api.models import Category, StorageLocation, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = '初期データを投入'
    
    def handle(self, *args, **kwargs):
        # ユーザー作成
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user(username='demo', password='demo1234')
            self.stdout.write('✓ デモユーザー作成')
        
        # カテゴリ作成
        categories = ['調味料', '飲料', '日用品', '冷凍食品', '缶詰', '生鮮食品']
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write('✓ カテゴリ作成')
        
        # 保管場所作成
        locations = [
            ('パントリー', '常温保存可能な食品や調味料'),
            ('冷蔵庫', '温度管理が必要な食品'),
            ('冷凍庫', '長期保存用'),
            ('キッチン棚', '調味料や日用品'),
        ]
        for name, desc in locations:
            StorageLocation.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
        self.stdout.write('✓ 保管場所作成')
        
        self.stdout.write(self.style.SUCCESS('初期データ投入完了'))
```

実行:
```bash
python manage.py init_data
```

## 11. 開発サーバー起動

```bash
python manage.py runserver
```

アクセス:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## 12. Dockerfileの更新

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# マイグレーション実行 + サーバー起動
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
```

## 13. まとめ

Django実装の主なポイント:

- **Models**: Django ORMを使用、`auto_now`/`auto_now_add`で自動更新
- **Serializers**: Pydanticの代わりにDRF Serializersを使用
- **Views**: ViewSetsで RESTful APIを実装
- **認証**: djangorestframework-simplejwtでJWT認証
- **マイグレーション**: `manage.py makemigrations`で自動生成

次のステップ: 完全なviews.pyとserializers.pyの実装
