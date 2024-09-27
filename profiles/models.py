from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model): 
    """ 
    Custom profile model extending Django's Auth Model Profile.
    Adds image and biography, last visited notifications,
    created at and updated at fields.
    """

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(blank=True)
    image = models.URLField(max_length=1024, default='https://picsum.photos/id/400/200')
    last_visited_notifications = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        """
        Return the string representation of the profile, which is the profilename.
        """
        return self.owner.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        # Set the username to the email when the User is created
        instance.username = instance.email
        # Save the User with the updated username
        instance.save()  
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)

class Follower(models.Model):
    """
    Model to represent profiles following each other. 
    Each instance records a profile following another profile.
    """

    followed_profile = models.ForeignKey (Profile, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey (Profile, on_delete=models.CASCADE, related_name='follower')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['followed_profile', 'follower'],
                name='unique_follower'
            )
        ]

    def __str__(self):
        """
        Return a string representation of the follow relationship.
        """
        return f'{self.follower} follows {self.followed_profile}'

