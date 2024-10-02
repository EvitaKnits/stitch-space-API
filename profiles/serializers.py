from profiles.models import Profile, Follower
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """
    Converts Profile objects into a format suitable for API responses.
    Includes owner-related data such as first name, last name, and email,
    as well as profile-specific fields like biography, followers, and pieces.
    Also handles updating both the `User` and `Profile` models.
    """
    firstName = serializers.CharField(source='owner.first_name')
    lastName = serializers.CharField(source='owner.last_name')
    email = serializers.EmailField(source='owner.email')
    lastVisitedNotifications = serializers.DateTimeField(
        source='last_visited_notifications'
    )
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    followers = serializers.IntegerField(source='followed_count',
                                        read_only=True)
    is_following = serializers.IntegerField(source='follower_count',
                                            read_only=True)
    pieces = serializers.IntegerField(source='pieces_count', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'firstName', 'lastName', 'email', 'biography', 'image',
            'lastVisitedNotifications', 'createdAt', 'updatedAt', 'followers',
            'is_following', 'pieces'
        ]

    def update(self, instance, validated_data):
        # Pop owner data to update the User model
        owner_data = validated_data.pop('owner', {})
        firstName = owner_data.get('first_name')
        lastName = owner_data.get('last_name')
        email = owner_data.get('email')

        # Update the User instance
        if firstName:
            instance.owner.first_name = firstName
        if lastName:
            instance.owner.last_name = lastName
        if email:
            instance.owner.email = email
            instance.owner.username = email
        instance.owner.save()

        # Update the Profile instance
        return super().update(instance, validated_data)


class FollowerSerializer(serializers.ModelSerializer):
    """
    Converts Follower objects into a format suitable for API responses.
    Includes related profile data for both 'followedProfile' and
    'followerProfile'. Dynamically controls the output based on the
    'view_type' context, omitting fields when appropriate (e.g.,
    'followers_only' or 'following_only').
    """
    followedProfile = ProfileSerializer(source='followed_profile', read_only=True)
    followerProfile = ProfileSerializer(source='follower',
                                        read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Follower
        fields = ['id', 'followedProfile', 'followerProfile', 'createdAt']

    def to_representation(self, instance):
        """
        Override the to_representation method to dynamically control the output
        """
        representation = super().to_representation(instance)

        # If context 'view_type' set to 'followers_only' omit 'followedProfile'
        if self.context.get('view_type') == 'followers_only':
            representation.pop('followedProfile', None)

        # If context 'view_type' set to 'following_only' omit 'followerProfile'
        if self.context.get('view_type') == 'following_only':
            representation.pop('followerProfile', None)

        return representation
