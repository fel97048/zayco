from django.db.models import F, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User,
    Category,
    StorageLocation,
    Product,
    InventoryLot,
    InventoryTransaction,
    ShoppingListItem,
)
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    CategorySerializer,
    StorageLocationSerializer,
    ProductSerializer,
    InventoryLotSerializer,
    InventoryTransactionSerializer,
    ShoppingListItemSerializer,
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'detail': 'ユーザー名とパスワードを入力してください'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return Response({'detail': 'ユーザー名またはパスワードが正しくありません'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'token_type': 'bearer',
        })


class UserMeView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        if category.products.exists():
            return Response({'detail': 'このカテゴリは商品で使用されているため削除できません'}, status=status.HTTP_409_CONFLICT)
        category.delete()
        return Response({'message': 'カテゴリを削除しました'})


class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all().order_by('name')
    serializer_class = StorageLocationSerializer
    http_method_names = ['get', 'post', 'delete']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(deleted_at__isnull=True).order_by('name')
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({'message': '商品を削除しました'})


class InventoryLotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryLot.objects.select_related('product', 'storage_location').all().order_by('product__name')
    serializer_class = InventoryLotSerializer


class PurchaseView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        expiry_date = request.data.get('expiry_date')
        storage_location_id = request.data.get('storage_location_id')

        if not product_id or quantity is None:
            return Response({'detail': 'product_id と quantity が必要です'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = float(quantity)
        except (TypeError, ValueError):
            return Response({'detail': 'quantity は数値で指定してください'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'detail': '数量は0.1以上で入力してください'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk=product_id, deleted_at__isnull=True)
        storage_location = product.default_storage_location
        if storage_location_id:
            storage_location = get_object_or_404(StorageLocation, pk=storage_location_id)

        lot, _ = InventoryLot.objects.get_or_create(
            product=product,
            storage_location=storage_location,
            expiry_date=expiry_date,
            defaults={'created_by': request.user, 'purchased_date': timezone.now().date()},
        )
        lot.quantity = F('quantity') + quantity
        lot.save()
        lot.refresh_from_db()

        InventoryTransaction.objects.create(
            lot=lot,
            product=product,
            user=request.user,
            product_name=product.name,
            transaction_type='購入',
            quantity=quantity,
            storage_location_name=storage_location.name,
            expiry_date=lot.expiry_date,
        )
        return Response(InventoryLotSerializer(lot).data, status=status.HTTP_201_CREATED)


class UseInventoryView(APIView):
    def post(self, request, pk):
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response({'detail': 'quantity が必要です'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = float(quantity)
        except (TypeError, ValueError):
            return Response({'detail': 'quantity は数値で指定してください'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'detail': '数量は0.1以上で入力してください'}, status=status.HTTP_400_BAD_REQUEST)

        lot = get_object_or_404(InventoryLot, pk=pk)
        if lot.quantity < quantity:
            return Response({'detail': '在庫数が不足しています'}, status=status.HTTP_400_BAD_REQUEST)

        lot.quantity = F('quantity') - quantity
        lot.save()
        lot.refresh_from_db()

        InventoryTransaction.objects.create(
            lot=lot,
            product=lot.product,
            user=request.user,
            product_name=lot.product.name,
            transaction_type='使用',
            quantity=quantity,
            storage_location_name=lot.storage_location.name,
            expiry_date=lot.expiry_date,
        )
        return Response(InventoryLotSerializer(lot).data)


class InventorySummaryView(APIView):
    def get(self, request):
        summary = (
            InventoryLot.objects
            .filter(product__deleted_at__isnull=True)
            .values('product', 'product__name', 'product__unit')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('product__name')
        )
        return Response([{
            'product_id': item['product'],
            'product_name': item['product__name'],
            'unit': item['product__unit'],
            'total_quantity': item['total_quantity'] or 0,
        } for item in summary])


class InventoryHistoryView(APIView):
    def get(self, request):
        transactions = InventoryTransaction.objects.all()[:100]
        serializer = InventoryTransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class ShoppingListItemViewSet(viewsets.ModelViewSet):
    queryset = ShoppingListItem.objects.select_related('product').all().order_by('-created_at')
    serializer_class = ShoppingListItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.filter(added_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
