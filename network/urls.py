from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("", views.all_posts, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like/<int:post_id>",views.like, name="like"),
    path("comment/<int:post_id>",views.comment, name="comment"),
    path("repost/<int:post_id>",views.repost, name="repost"),
    path("delete/<int:post_id>",views.delete, name="delete"),
    path("edit/<int:post_id>",views.edit_post, name="edit"),
    path("bookmark/<int:post_id>",views.bookmark, name="bookmark"),
    path("post/<int:post_id>",views.view_post, name="post"),
    path("bookmark",views.view_bookmarks, name="bookmark"),
    path("profile/<str:username>",views.ProfileView.as_view(), name="profile"),
    path("following",views.following, name="following"),
]
