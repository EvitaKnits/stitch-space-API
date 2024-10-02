from django.contrib import admin
from notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    """
    Custom admin class to manage notifications in the admin interface.
    """
    list_display = (
        'id',
        'actor',
        'recipient',
        'interaction_type',
        'piece_title',
        'created_at'
    )
    list_filter = ('interaction_type', 'created_at')
    search_fields = ('actor__username', 'recipient__username', 'piece__title')
    ordering = ('-created_at',)

    def piece_title(self, obj):
        """
        Display the title of the piece, or '-' if no piece is associated (for
        'follow' interaction).
        """
        return obj.piece.title if obj.piece else '-'

    piece_title.short_description = 'Piece'

    def save_model(self, request, obj, form, change):
        """
        Custom save logic if needed. Currently, just using the parent save
        method.
        """
        super().save_model(request, obj, form, change)


# Register the notification model
admin.site.register(Notification, NotificationAdmin)
