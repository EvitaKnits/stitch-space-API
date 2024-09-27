from django.contrib import admin
from pieces.models import Piece, Comment, Rating

class PieceAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Piece model.
    """
    list_display = ('id', 'title', 'profile', 'art_type', 'featured', 'created_at', 'updated_at')
    list_filter = ('art_type', 'created_at')
    search_fields = ('title', 'profile__profilename', 'art_type')
    ordering = ('-created_at',)
    
    def save_model(self, request, obj, form, change):
        """
        Custom save logic for Piece model if needed.
        """
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Comment model.
    """
    list_display = ('id', 'piece_title', 'profile', 'created_at', 'content_short')
    list_filter = ('created_at',)
    search_fields = ('content', 'piece__title', 'profile__profilename')
    ordering = ('-created_at',)

    def content_short(self, obj):
        """
        Display a shortened version of the comment content.
        """
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_short.short_description = 'Comment'

    def piece_title(self, obj):
        """
        Display the title of the piece associated with the rating
        """
        return obj.piece.title

class RatingAdmin(admin.ModelAdmin):
    """
    Custom admin class for the Rating model.
    """
    list_display = ('id', 'piece_title', 'profile', 'score', 'created_at', 'updated_at')
    fields = ('piece', 'profile', 'score')
    list_filter = ('score', 'created_at')
    search_fields = ('piece__title', 'profile__profilename', 'score')
    ordering = ('-created_at',)

    def piece_title(self, obj):
        """
        Display the title of the piece associated with the rating
        """
        return obj.piece.title
    
    def save_model(self, request, obj, form, change):
        """
        Custom save logic for Rating model if needed.
        """
        super().save_model(request, obj, form, change)

# Register the models with the admin site
admin.site.register(Piece, PieceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, RatingAdmin)
