from django import template

register = template.Library()

@register.filter
def is_reposted_by_user(post, user):
    return post.is_reposted(user)