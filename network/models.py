from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User model. also contain the profile picture. """
    picture = models.ImageField(upload_to="network/images/profile_pictures", blank=True, null=True)


class post(models.Model):
    """ Post model. Each post has a user, content, timestamp, and likes. """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
        }
        