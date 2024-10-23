from django.contrib import admin

from users.models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'is_staff', 'is_superuser', 'is_active',)
    search_fields = ('email',)
    list_display = ('email', 'id', 'is_staff', 'is_superuser', 'is_active',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    # list_filter = ('id', 'user', 'course', 'created_at',)
    # search_fields = ('course',)
    list_display = ('id', 'user', 'course', 'created_at',)
