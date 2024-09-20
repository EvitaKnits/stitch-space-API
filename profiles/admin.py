from django.contrib import admin
from profiles.models import Profile, Follower

class ProfileAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Profile model to manage profiles in the admin
    interface.
    """
    list_display = (
        'id',
        'created_at',
        'updated_at',
    )
    fields = (
        'id',
        'biography',
    )
    readonly_fields = ('id', 'last_visited_notifications')
    search_fields = ('first_name', 'last_name')
    ordering = ('id',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

class FollowerAdmin(admin.ModelAdmin):
    """
    Admin class for the Follower model to manage follower relationships.
    """
    list_display = ('follower', 'followed_profile', 'created_at')
    search_fields = ('follower__profilename', 'followed_profile__profilename')
    list_filter = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

# Register the models with the admin site
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follower, FollowerAdmin)