from django import template

from analytic.models import LikeHistory

register = template.Library()


@register.filter
def to_range(value):
    return range(value)


@register.simple_tag
def has_liked_by(user, property):
    return LikeHistory.objects.filter(user=user, property=property).exists()


@register.simple_tag
def has_review_by(user, property):
    return property.reviews.filter(user=user).exists()
