from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'is_staff', 'is_superuser', 'is_active',)
    search_fields = ('email',)
    list_display = ('email', 'id', 'is_staff', 'is_superuser', 'is_active',)
