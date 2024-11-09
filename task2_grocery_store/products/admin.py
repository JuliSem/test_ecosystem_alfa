from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Админ-панель модели продуктов.'''

    list_display = ('id', 'name', 'slug', 'category_display',
                    'subcategory_display', 'get_original_image',
                    'quantity', 'price')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'category_display', 'subcategory_display')
    readonly_fields = ('get_original_image', )
    prepopulated_fields = {'slug': ('name',)}

    def category_display(self, obj):
        return str(obj.category.name)

    def subcategory_display(self, obj):
        return str(obj.subcategory.name)

    def get_original_image(self, obj):
        '''Получение миниатюры изображения.'''
        return mark_safe(f"<img src='{obj.original_image.url}' width=50")

    category_display.short_description = 'Категория'
    subcategory_display.short_description = 'Подкатегория'
    get_original_image.short_description = 'Изображение'
