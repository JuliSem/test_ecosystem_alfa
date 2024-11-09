from django.contrib import admin

from carts.models import Cart, CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    '''Админ-панель для элементов корзины.'''

    list_display = ('cart', 'product_display', 'quantity')
    list_filter = ('cart', 'product')

    def product_display(self, obj):
        return str(obj.product.name)

    product_display.short_description = 'Продукт'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Админ-панель для корзины.'''

    list_display = (
        'user_display',
        'created_at',
        'updated_at',
    )
    list_filter = ('user', )

    def user_display(self, obj):
        return str(obj.user)

    user_display.short_description = 'Пользователь'
