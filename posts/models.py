from django.contrib.auth.models import User
from django.db import models


class StandardModel(models.Model):
    created_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(StandardModel):
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(max_length=10000, blank=False)


class Comment(StandardModel):
    body = models.TextField(max_length=1000, blank=False)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
