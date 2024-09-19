from pieces.models import Piece, Comment, Rating
from users.models import User 
from rest_framework import serializers

class PieceSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    artType = serializers.CharField(source='art_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Piece
        fields = [
            'id', 'title', 'image', 'user', 'artType',
            'createdAt', 'updatedAt'
        ]

class CommentSerializer(serializers.ModelSerializer): 
    piece = serializers.PrimaryKeyRelatedField(queryset=Piece.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'piece', 'user', 'createdAt'
        ]


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    piece = serializers.PrimaryKeyRelatedField(queryset=Piece.objects.all())
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id', 'user', 'piece', 'score', 'createdAt', 'updatedAt'
        ]