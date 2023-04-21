from django import template

register = template.Library()

@register.filter
def is_reposted_by_user(post, user):
    return post.is_reposted(user)

@register.filter
def is_repost(post):
    return post.is_a_repost()