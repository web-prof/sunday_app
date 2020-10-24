from django import template
from core.models import *

register = template.Library()


@register.filter()
def score_counter(user):
    if user.is_authenticated:
        prof = Profile.objects.get(user=user)
        res = Results.objects.filter(profile=prof,is_correct=True)
        if res.exists():
            return res.count()
    return 0