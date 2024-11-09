from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    '''Админ-панель для пользователя.'''

    list_display = ('username', 'first_name', 'last_name',
                    'email', 'phone_number')
    list_display_links = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name',
                     'email', 'phone_number')
