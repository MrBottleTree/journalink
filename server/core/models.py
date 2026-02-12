from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    class Category(models.TextChoices):
        BLOG = "BLOG", "Blog"
        ANNOUNCEMENT = "ANNOUNCEMENT", "Announcement"
        MEDIA = "MEDIA", "Media"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author.username} ({self.category})"

class StarredPost(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="starred_posts"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="starred_by"
    )
    starred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} starred {self.post.id}"


class PostTag(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="tagged_users"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tagged_posts"
    )

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} tagged in Post {self.post.id}"
