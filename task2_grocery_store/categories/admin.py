from django.contrib import admin
from django.utils.safestring import mark_safe

from categories.models import Category, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Админ-панель для модели категории.'''

    list_display = ('id', 'name', 'slug', 'get_image')
    list_display_links = ('name', )
    readonly_fields = ('get_image', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

    def get_image(self, obj):
        '''Получение миниатюры изображения.'''
        return mark_safe(f"<img src='{obj.image.url}' width=50>")

    get_image.short_description = 'Изображение'


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    '''Админ-панель для модели подкатегории.'''

    list_display = ('category_display', 'name', 'slug', 'get_image')
    search_fields = ('category', 'name' )
    readonly_fields = ('get_image', )
    prepopulated_fields = {'slug': ('name',)}

    def category_display(self, obj):
        return str(obj.category.name)

    def get_image(self, obj):
        '''Получение миниатюры изображения.'''
        return mark_safe(f"<img src='{obj.image.url}' width=50>")

    category_display.short_description = 'Категория'
    get_image.short_description = 'Изображение'
