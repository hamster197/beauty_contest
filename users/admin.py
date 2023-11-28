from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MainUser


# Register your models here.
@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'last_name', 'first_name', 'email', 'is_active', )
    list_filter = ('is_active', 'groups', )
    search_fields = ('username', 'email', 'last_name', 'groups',)
    search_help_text = 'введите логин, email или фамилию для поиска'
    ordering = ('-pk',)