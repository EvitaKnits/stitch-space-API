from profiles.models import Profile, Follower
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='owner.first_name')
    lastName = serializers.CharField(source='owner.last_name')
    email = serializers.EmailField(source='owner.email')
    artType = serializers.CharField(source='art_type')
    lastVisitedNotifications = serializers.DateTimeField(
        source='last_visited_notifications', read_only=True
    )
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'firstName', 'lastName', 'email', 'biography', 'image',
            'artType', 'lastVisitedNotifications', 'createdAt', 'updatedAt'
        ]

    def update(self, instance, validated_data):
        # Pop owner data to update the User model
        owner_data = validated_data.pop('owner', {})
        first_name = owner_data.get('first_name')
        last_name = owner_data.get('last_name')
        email = owner_data.get('email')

        # Update the User instance
        if first_name:
            instance.owner.first_name = first_name
        if last_name:
            instance.owner.last_name = last_name
        if email:
            instance.owner.email = email
        instance.owner.save()

        # Update the Profile instance
        return super().update(instance, validated_data)

class FollowerSerializer(serializers.ModelSerializer): 
    followedProfile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='followed_profile')
    follower = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta: 
        model = Follower
        fields = ['id', 'followedProfile', 'follower', 'createdAt']