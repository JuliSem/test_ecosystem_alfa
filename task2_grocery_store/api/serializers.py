from django.conf import settings
from rest_framework import serializers
from rest_framework.request import Request

from categories.models import Category, Subcategory
from products.models import Product
from carts.models import Cart, CartItem


class SubcategoryListSerializer(serializers.ModelSerializer):
    '''Serializer для получения подкатегории/ подкатегорий.'''

    class Meta:
        model = Subcategory
        fields = ('name', 'slug')


class CategoryListSerializer(serializers.ModelSerializer):
    '''Serializer для получения категории/ категорий.'''

    subcategories = SubcategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'subcategories')


class ProductListSerializer(serializers.ModelSerializer):
    '''Serializer для получения продукта/ продуктов.'''

    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory',
                  'price', 'images')
        
    def get_images(self, obj):
        '''Получение списка изображений продукта.'''

        request = self.context.get('request')
        if not isinstance(request, Request):
            return []
        base_url = request.build_absolute_uri(settings.MEDIA_URL)
        return [
            base_url + str(obj.original_image),
            base_url + str(obj.small_image),
            base_url + str(obj.big_image),
        ]


class CartItemSerializer(serializers.ModelSerializer):
    '''Serializer для элементов корзины.'''

    product = serializers.CharField(source='product.name')
    class Meta:
        model = CartItem
        fields = ('product', 'quantity')


class ShortCartItemSerializer(serializers.ModelSerializer):
    '''Укороченный serializer для элементов корзины.'''

    product = serializers.CharField(source='product.name')

    class Meta:
        model = CartItem
        fields = ('product', )


class CartSerializer(serializers.ModelSerializer):
    '''Serializer для корзины.'''

    user = serializers.ReadOnlyField(source='user.username')
    items = CartItemSerializer(many=True, read_only=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('user', 'items', 'total_quantity', 'total_price')

    # @staticmethod
    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())

    # @staticmethod
    def get_total_price(self, obj):
        return sum(
            item.product.price * item.quantity for item in obj.items.all()
        )
