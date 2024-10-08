from pieces.models import Piece, Comment, Rating
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework import serializers


class PieceSerializer(serializers.ModelSerializer):
    """
    Converts Piece objects into a format suitable for API responses.
    It provides additional related data for the associated 'profile'
    and 'userRating' fields using custom methods to include nested
    data from other models such as `Profile` and `Rating`.
    """
    profile = ProfileSerializer(read_only=True)
    artType = serializers.CharField(source='art_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    rating = serializers.FloatField(source='avg_rating', read_only=True)
    userRating = serializers.SerializerMethodField()
    userName = serializers.ReadOnlyField(source='owner.username')
    featured = serializers.BooleanField(read_only=True)

    class Meta:
        model = Piece
        fields = [
            'id', 'title', 'image', 'profile', 'artType',
            'createdAt', 'updatedAt', 'rating', 'userRating',
            'userName', 'featured'
        ]

    def get_userRating(self, obj):
        if hasattr(obj, 'user_rating') and obj.user_rating:
            return RatingSerializer(obj.user_rating).data
        return None


class CommentSerializer(serializers.ModelSerializer):
    """
    Converts Comment objects into a format suitable for API responses.
    It provides additional related data for the associated 'profile'
    field using a custom method to include nested data from the `Profile` model
    """
    piece = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'piece', 'profile', 'createdAt'
        ]

    def get_profile(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return ProfileSerializer(obj.profile).data
        return None


class RatingSerializer(serializers.ModelSerializer):
    """
    Converts Rating objects into a format suitable for API responses.
    Includes related 'profile' and 'piece' fields as primary keys and
    provides timestamps for creation and last update.
    """
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    piece = serializers.PrimaryKeyRelatedField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id', 'profile', 'piece', 'score', 'createdAt', 'updatedAt'
        ]
