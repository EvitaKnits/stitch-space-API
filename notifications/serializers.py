from notifications.models import Notification
from pieces.models import Piece
from pieces.serializers import PieceSerializer
from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    """
    Converts Notification objects into a format suitable for API responses.
    It provides additional related data for the associated 'piece', 'actor',
    and 'recipient' fields using custom methods to include nested data from
    other models such as `Piece` and `Profile`.
    """
    piece = serializers.SerializerMethodField()
    actor = serializers.SerializerMethodField()
    recipient = serializers.SerializerMethodField()
    interactionType = serializers.CharField(source='interaction_type')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'piece', 'actor', 'recipient', 'interactionType', 'createdAt'
        ]

    def get_piece(self, obj):
        if hasattr(obj, 'piece') and obj.piece:
            return PieceSerializer(obj.piece).data
        return None

    def get_actor(self, obj):
        if hasattr(obj, 'actor') and obj.actor:
            return ProfileSerializer(obj.actor).data
        return None

    def get_recipient(self, obj):
        if hasattr(obj, 'recipient') and obj.recipient:
            return ProfileSerializer(obj.recipient).data
        return None
