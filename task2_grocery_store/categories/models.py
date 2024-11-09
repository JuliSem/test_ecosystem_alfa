from django.db import models

from utils import generic_image_path


class Category(models.Model):
    '''Модель для категории.'''

    name = models.CharField(
        verbose_name='Категория',
        max_length=150,
        unique=True
    )
    slug = models.CharField(
        verbose_name='URL',
        max_length=150,
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=generic_image_path,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ('id', )

    def __str__(self) -> str:
        return f'Категория: {self.name}'


class Subcategory(models.Model):
    '''Модель для подкатегории.'''

    category = models.ForeignKey(
        to=Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(
        verbose_name='Подкатегория',
        max_length=150,
        unique=True
    )
    slug = models.CharField(
        verbose_name='URL',
        max_length=150,
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=generic_image_path,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Подкатегорию'
        verbose_name_plural = 'Подкатегории'
        ordering = ('id', )

    def __str__(self) -> str:
        return f'Подкатегория: {self.name}'
