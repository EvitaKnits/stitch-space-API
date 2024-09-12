from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """
    Custom admin class for the User model to manage users in the admin
    interface.
    """
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'created_at',
        'updated_at',
    )
    fields = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'groups',
    )
    readonly_fields = ('id', 'last_login', 'last_visited_notifications')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ('groups',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register the User model
admin.site.register(User, UserAdmin)