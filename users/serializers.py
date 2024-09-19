from users.models import User, Follower
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    artType = serializers.CharField(source='art_type')
    lastVisitedNotifications = serializers.DateTimeField(source='last_visited_notifications', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'firstName', 'lastName', 'email', 'password', 'biography', 'image',
            'artType', 'lastVisitedNotifications', 'createdAt', 'updatedAt'
            ] 

class FollowerSerializer(serializers.ModelSerializer): 
    followedUser = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='followed_user')
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta: 
        model = Follower
        fields = ['id', 'followedUser', 'follower', 'createdAt']