from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.urls import reverse,reverse_lazy

from .models import User,Post

@login_required
class ProfileView(View):
    # Get a users's profile
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            posts = Post.objects.filter(user=user).order_by("timestamp").all()
            picture = user.picture.url
            return render(request, "network/profile.html", {
                "user": user,
                "posts": posts,
                "picture": picture
            })
        except User.DoesNotExist:
            # Handle user not found error
            return render(request, "network/error.html", {
                "error": "User does not exist."
            })
            
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
            # If the user is trying to follow or unfollow
            # Follow a user
            if request.POST["follow"] == "follow":
                request.user.follow(user)
                return HttpResponseRedirect(reverse_lazy("profile", args=[username]))
            # Unfollow a user
            elif request.POST["follow"] == "unfollow":
                request.user.unfollow(user)
                return HttpResponseRedirect(reverse_lazy("profile", args=[username]))
        except User.DoesNotExist:
            # Handle user not found error
            return render(request, "network/error.html", {
                "error": "User does not exist."
            })
            

def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@login_required
def new_post(request):
    # If the user is submitting a new post
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")
    
def all_posts(request):
    # Get all posts
    posts = Post.objects.order_by("timestamp").all()
    return render(request, "network/all_posts.html", {
        "posts": posts
    })
    
@login_required
def following_posts(request):
    # Get all posts from users that the current user is following
    posts = Post.objects.filter(user__in=request.user.following.all()).order_by("timestamp").all()
    return render(request, "network/following_posts.html", {
        "posts": posts
    })
    

