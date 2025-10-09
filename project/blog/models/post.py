from django.db import models
from django.contrib.auth.models import User
from .category import Category
from .tag import Tag


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to="post/%Y/%m/%d", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title