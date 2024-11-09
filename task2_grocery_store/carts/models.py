from django.db import models

from products.models import Product
from users.models import User


class Cart(models.Model):
    '''Модель для козины.'''

    user = models.OneToOneField(
        to=User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'
        ordering = ('id', )

    def __str__(self):
         return f'Корзина {self.user.username}'


class CartItem(models.Model):
    '''Модель для элементов корзины.'''

    cart = models.ForeignKey(
        to=Cart,
        verbose_name='Корзина',
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        to=Product,
        verbose_name='Товар',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        ordering = ('id', )


    def __str__(self):
        return (f'Корзина {self.cart.user.username} | '
                f'Товар {self.product.name} | '
                f'Количество {self.quantity}')
