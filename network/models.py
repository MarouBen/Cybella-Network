from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User model. also contain the profile picture. and it's followers and following. """
    picture = models.ImageField(upload_to="network/images/profile_pictures", blank=True, null=True,default="network/images/profile_pictures/default.png")
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")
    bookmarks = models.ManyToManyField("Post", blank=True, related_name="bookmarked_by")
    
    def follow(self, user):
        """ Follow the given user """
        self.following.add(user)
    
    def unfollow(self, user):
        """ Unflow the given user """
        self.following.remove(user)
        
    def is_following(self, user):
        """ Check if the current user is following the given user """
        return self.following.filter(pk=user.pk).exists()
    
    
    def get_followers(self):
        """ Return all followers """
        return self.followers.all()
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "picture": self.picture.url,
            "followers": self.number_followers(),
            "following": self.number_following(),
        }
    
    def __str__(self):
        return f"{self.username}"
    



class Post(models.Model):
    """ Post model. Each post has a user, content, timestamp, likes and images. """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    images = models.ImageField(upload_to="network/images/posts", blank=True, null=True)
    repost = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="reposts")
    parent_post = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.count(),
        }
    
    def add_like(self, user):
        """ Add user to likes """
        return self.likes.add(user)
        
    def remove_like(self, user):
        """ Remove user from likes """
        return self.likes.remove(user)
        
    def get_likers(self):
        """" Return List of all likers """
        return self.likes.all()
    
    def number_likes(self):
        """ Return number of likes """
        return self.likes.count()
    
    def is_reposted(self, user):
        """ Return True if user reposted """
        return self.reposts.filter(user=user).exists()
    
    def is_a_repost(self):
        """ Return True if post is a repost """
        return self.repost is not None and self.user != self.repost.user 
    
    def __str__(self):
        return f"{self.user.username}'s post ({self.id})"
        