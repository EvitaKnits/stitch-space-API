from pieces.models import Piece, Comment, Rating
from profiles.models import Profile 
from rest_framework import serializers

class PieceSerializer(serializers.ModelSerializer): 
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    artType = serializers.CharField(source='art_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    rating = serializers.FloatField(source='avg_rating', read_only=True)

    class Meta:
        model = Piece
        fields = [
            'id', 'title', 'image', 'profile', 'artType',
            'createdAt', 'updatedAt', 'rating'
        ]

class CommentSerializer(serializers.ModelSerializer):
    piece = serializers.PrimaryKeyRelatedField(read_only=True)
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'piece', 'profile', 'createdAt'
        ]


class RatingSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    piece = serializers.PrimaryKeyRelatedField(read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id', 'profile', 'piece', 'score', 'createdAt', 'updatedAt'
        ]