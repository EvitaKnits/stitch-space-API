from notifications.models import Notification
from pieces.models import Piece
from users.models import User
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer): 
    piece = serializers.PrimaryKeyRelatedField(queryset=Piece.objects.all())
    actor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    interactionType = serializers.CharField(source='interaction_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta: 
        model = Notification
        fields = [
            'id', 'piece', 'actor', 'recipient', 'interactionType', 'createdAt'
        ]