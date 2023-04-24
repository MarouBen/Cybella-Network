import json
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse,reverse_lazy
from newsapi import NewsApiClient

from .models import User,Post

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    # Get a users's profile
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            posts = Post.objects.filter(user=user).order_by("-timestamp").all().filter(parent_post=None)
            replys = Post.objects.filter(user=user).order_by("-timestamp").all().exclude(parent_post=None)
            picture = user.picture.url
            # Paginate posts with 10 posts per page
            paginator = Paginator(posts, 10)
            page = request.GET.get('page')
            posts = paginator.get_page(page)
            return render(request, "network/profile.html", {
                "TheUser": user,
                "posts": posts,
                "replys": replys,
                "picture": picture
            })
        except User.DoesNotExist:
            # Handle user not found error
            return render(request, "network/error.html", {
                "error": "User does not exist."
            })
            
    # Follow or unfollow a user  
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)  
            # Check if user already follows
            if request.user.is_following(user):
                request.user.unfollow(user)
                return JsonResponse({'success': True, 'message': 'Unfollowed successfully.'})
            
            else :
                request.user.follow(user)
                return JsonResponse({'success': True, 'message': 'Followed successfully.'})
        except User.DoesNotExist:
            # Handle user not found error
            return JsonResponse({'Error': False, 'message': 'User Not Found.'})
    
    
@login_required    
def edit_profile(request, username):
        userObject = User.objects.get(username=username)
        
        if request.user != userObject:
            raise PermissionDenied
       
        if request.method == "POST":
            if request.FILES.get("I") is not None:
                # delete old profile picture if it exists
                if userObject.picture:
                    default_storage.delete(userObject.picture.name)
                    # save new profile picture
                    userObject.picture = request.FILES["I"]
                    
            if request.POST.get("username") is not None:
                userObject.username = request.POST.get("username")
            if request.POST.get("email") is not None:
                userObject.email = request.POST.get("email")
            if request.POST.get("bio") is not None:
                userObject.bio = request.POST.get("bio")
            userObject.save()
            return HttpResponseRedirect(reverse("profile", args=[userObject.username]))

        
    
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
            return JsonResponse({'Error': False, 'message': 'Invalid email and/or password.'})
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return JsonResponse({'Error': False, 'message': 'Passwords must match.'})

        # Attempt to create new user
        try:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'Error': False, 'message': 'Email address already taken.'})
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return JsonResponse({'Error': False, 'message': 'Username already taken.'})

        login(request, user)
        return JsonResponse({'success': True, 'redirect': reverse("index")})

    else:
        return render(request, "network/login.html")
    
@login_required
def new_post(request):
    # If the user is submitting a new post
    if request.method == "POST":
        image = request.FILES.get("I", None)
        content = request.POST.get("content", "")
        user = request.user
        post = Post(user=user, content=content, images=image)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")
    
def all_posts(request):
    # If the user is submitting a new post
    if request.method == "POST":
        if request.user.is_authenticated:
            return new_post(request)
        else: 
            # redirect to login page
            return HttpResponseRedirect(reverse("login"))
            
    # Get all posts
    posts_list = Post.objects.order_by("-timestamp").all().filter(parent_post=None)
    # Paginate posts with 10 posts per page
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, "network/all_posts.html", {
        "posts": posts
    })
    
    
@login_required
def following_posts(request):
    # Get all posts from users that the current user is following
    posts_list = Post.objects.filter(user__in=request.user.following.all()).order_by("timestamp").all()
    # Paginate posts with 10 posts per page
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, "network/following_posts.html", {
        "posts": posts
    })
    
@login_required
def edit_post(request, post_id):
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user is authorized to edit the post
    if post.user != request.user:
        raise PermissionDenied("You are not authorized to edit this post.")
    
    # If the user is submitting an edit
    if request.method == "POST":
        content = request.POST.get("content", "")
        post.content = content
        image = request.FILES.get("E_I", None)
        if  image != None:
            post.images = request.FILES.get("E_I", None)
        post.save()
        return HttpResponseRedirect(reverse("index"))
        
    

def like (request, post_id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a post."}, status=403)

    # Get the post
    post = get_object_or_404(Post, id=post_id)
    # If the user has already liked the post, unlike it
    if not request.user in post.likes.all():
        post.add_like(request.user)
        return JsonResponse({"message": "Post liked successfully."}, status=201)
    # If the user has not liked the post, like it
    else:
        post.remove_like(request.user)
        return JsonResponse({"message": "Post unliked successfully."}, status=201)
    
    
@login_required
def comment(request, post_id):
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    # If the user is submitting a comment
    if request.method == "POST":
        content = request.POST.get("content", "")
        images = request.FILES.get("R_I", None)
        user = request.user
        
        # create comment
        comment = Post(user=user, images=images, content=content, parent_post=post)
        comment.save()
        return HttpResponseRedirect(reverse("post", args=[post_id]))     
        

# function to repost a post
def repost(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a post."}, status=403)
    # Get the post
    original_post = get_object_or_404(Post, id=post_id)
    # If the user is submitting a repost
    user = request.user
    # unpost if already reposted
    if Post.objects.filter(user=user, repost=original_post).exists():
        Post.objects.filter(user=user, repost=original_post).delete()
        return JsonResponse({"message": "Post unposted successfully."}, status=201)
    else:
        repost = Post(user=user, content=f"Reposted from {original_post.user.username}: {original_post.content}", images=original_post.images, repost=original_post)
        repost.save()
        return JsonResponse({"message": "Post reposted successfully."}, status=201)
    
# function to delete a post
def delete(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged."}, status=403)
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    # delete if the user is the owner of the post
    if post.user == user:
        post.delete()
        return JsonResponse({"message": "Post deleted successfully."}, status=201)
    else:
        return JsonResponse({"error": "You are not authorized to delete this post."}, status=402)
    
# function to bookmark a post
def bookmark(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in to like a post."}, status=403)
    # Get the post
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if not post in user.bookmarks.all():
        user.bookmarks.add(post)
        return JsonResponse({"message": "Post bookmarked successfully."}, status=201)
    else:
        user.bookmarks.remove(post)
        return JsonResponse({"message": "Post unbookmarked successfully."}, status=201)
    
# function to view a post
def view_post(request,post_id):
    #get the post
    post = get_object_or_404(Post, id=post_id)
    # get the comments
    comments = Post.objects.filter(parent_post=post).order_by("-timestamp").all()
    return render(request, "network/post.html", {
        "comments": comments,
        "post": post
    }) 

# function to view bookmarks
def view_bookmarks(request):
    # get the bookmarks
    bookmarks = request.user.bookmarks.all()
    return render(request, "network/bookmark.html", {
        "posts": bookmarks
    })
    
# function that show post from following users
@login_required
def following(request):
    user = request.user
    # get the posts from following users
    posts = Post.objects.filter(user__in=user.following.all()).order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, "network/following.html", {
        "posts" : posts
    })
    
# News API
def news(request):
    # your existing view code
    newsapi = NewsApiClient(api_key='23057fa75f114ffaac8274b12da31e41')
    top_headlines = newsapi.get_top_headlines(language='en', country='us')
    articles = top_headlines['articles']
    response_data = {
        'articles': articles,
    }
    return JsonResponse(response_data)