from django.db import models
from django.contrib.auth.models import User

# todo list
from django.template.defaultfilters import slugify

"""
- captcha on comments
- use glow thingy on gitkraken
"""


class Post(models.Model):
    """
    # todo: comments, tags
    """

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
