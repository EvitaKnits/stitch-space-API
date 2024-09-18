from django.contrib import admin
from users.models import User, Follower

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
        'biography',
        'groups',
        'art_type',
    )
    readonly_fields = ('id', 'last_login', 'last_visited_notifications')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('id',)
    filter_horizontal = ('groups',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class FollowerAdmin(admin.ModelAdmin):
    """
    Admin class for the Follower model to manage follower relationships.
    """
    list_display = ('follower', 'followed_user', 'created_at')
    search_fields = ('follower__username', 'followed_user__username')
    list_filter = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Follower, FollowerAdmin)