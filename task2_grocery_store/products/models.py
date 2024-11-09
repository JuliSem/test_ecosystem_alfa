from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from categories.models import Category, Subcategory
from utils import generic_image_path


class Product(models.Model):
    '''Модель для продукта.'''

    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    subcategory = models.ForeignKey(
        to=Subcategory,
        verbose_name='Подкатегория',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    slug = models.CharField(
        verbose_name='URL',
        max_length=150,
        blank=True,
        null=True
    )
    original_image = models.ImageField(
        verbose_name='Оригинальное изображение',
        upload_to=generic_image_path,
        blank=True,
        null=True
    )
    small_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(width=100, height=100)],
        format='JPEG',
        options={'quality': 60}
    )
    big_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFill(width=400, height=400)],
        format='JPEG',
        options={'quality': 80}
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        default=0
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal(0.01),
                message='Цена на продукт не может быть отрицательной '
                        'или равняться 0!'
            ),
        ]
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id', )

    def __str__(self):
        return (f'Продукт: {self.name} | '
                f'Категория: {self.category.name} | '
                f'Подкатегория: {self.subcategory.name}')
