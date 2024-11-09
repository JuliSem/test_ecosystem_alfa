from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.paginations import LimitPagination
from api.serializers import (
    CartItemSerializer,
    CartSerializer,
    CategoryListSerializer,
    ProductListSerializer,
    ShortCartItemSerializer
)
from carts.models import Cart, CartItem
from categories.models import Category
from products.models import Product


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''ViewSet для получения категории/ категорий.'''

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = LimitPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    '''ViewSet для получения продукта/ продуктов.'''

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = LimitPagination

class CartViewSet(viewsets.ViewSet):
    '''ViewSet для корзины.'''

    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        '''
        Получение корзины текущего пользователя или создание, если её ещё нет.
        '''
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def list(self, request):
        '''Получение содержимого корзины текущего пользователя.'''
        cart = self.get_queryset()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    
    @staticmethod
    def get_product(product_name):
        '''Возвращает продукт по его названию.'''

        try:
            product = Product.objects.get(name=product_name)
            return product
        except Product.DoesNotExist:
            return Response(
                {
                    'error': f'Товара с названием {product_name} не существует!'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
    @staticmethod
    def get_cart_item(cart, product):
        '''Возвращает элемент корзины по корзине и продукту.'''

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            return cart_item
        except CartItem.DoesNotExist:
            return Response(
                {
                    'error': f'Элемент корзины c названием {product.name} не существует'
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(request=CartItemSerializer, )
    @action(detail=False, methods=['POST', ])
    def add_item(self, request):
        '''Добавляет продукт в корзину текущего пользователя.'''
        
        product = self.get_product(request.data.get('product'))
        cart = self.get_queryset()
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        cart_item.quantity += int(
            request.data.get(
                'quantity', 0
            )
        )
        cart_item.save()
        return Response(data=CartSerializer(cart).data)

    @extend_schema(request=ShortCartItemSerializer, )
    @action(detail=False, methods=['DELETE', ])
    def delete_item(self, request):
        '''Удаляет продукт из корзины текущего пользователя.'''

        cart = self.get_queryset()
        product = self.get_product(product_name=request.data.get('product'))
        cart_item = self.get_cart_item(cart=cart, product=product)
        cart_item.delete()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    
    @extend_schema(request=CartItemSerializer, )
    @action(detail=False, methods=['PATCH', ])
    def update_item(self, request):
        '''
        Обновляет количество продуктов в корзине текущего пользователя.
        '''

        cart = self.get_queryset()
        product = self.get_product(product_name=request.data.get('product'))
        cart_item = self.get_cart_item(cart=cart, product=product)
        quantity = request.data.get('quantity')
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
    
    @action(detail=False, methods=['DELETE', ])
    def clear_cart(self, request):
        '''Полностью очищает корзину текущего пользователя.'''

        cart = self.get_queryset()
        cart.items.all().delete()
        serializer = CartSerializer(cart)
        return Response(data=serializer.data)
