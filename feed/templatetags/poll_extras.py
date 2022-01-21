from django import template

register = template.Library()

@register.filter
def on_user(likes, user_id):
    return likes.filter(user = user_id)[0].vote