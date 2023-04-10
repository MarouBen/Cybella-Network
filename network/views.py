import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator
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
            # Paginate posts with 10 posts per page
            paginator = Paginator(posts, 10)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
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
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect': reverse("index")})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email and/or password.'})
    else:
        return render(request, "mail/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return JsonResponse({'success': False, 'message': 'Passwords must match.'})

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Email address already taken.'})

        login(request, user)
        return JsonResponse({'success': True, 'redirect': reverse("index")})

    else:
        return render(request, "mail/login.html")
    
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
    # Paginate posts with 10 posts per page
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/all_posts.html", {
        "posts": posts
    })
    
@login_required
def following_posts(request):
    # Get all posts from users that the current user is following
    posts = Post.objects.filter(user__in=request.user.following.all()).order_by("timestamp").all()
    # Paginate posts with 10 posts per page
    paginator = Paginator(following_posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "network/following_posts.html", {
        "posts": posts
    })
    
@login_required
def edit_post(request, post_id):
    try:
        # Get the post
        post = Post.objects.get(id=post_id)
        
        # Check if the user is authorized to edit the post
        if post.user != request.user:
            return JsonResponse({"error": "You are not authorized to edit this post."}, status=403)
        
        # If the user is submitting an edit
        if request.method == "POST":
            data = json.loads(request.body)
            content = data.get("content", "")
            post.content = content
            post.save()
            return JsonResponse({"message": "Post edited successfully."}, status=201)
        
    # Handle post not found error
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
@login_required
def like (request, post_id):
    try:
        # Get the post
        post = Post.objects.get(id=post_id)
        # If the user has already liked the post, unlike it
        if request.user in post.likes.all():
            post.add_like(request.user)
            return JsonResponse({"message": "Post liked successfully."}, status=201)
        # If the user has not liked the post, like it
        else:
            post.remove_like(request.user)
            return JsonResponse({"message": "Post unliked successfully."}, status=201)
    # Handle post not found error
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
