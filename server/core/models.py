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

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class StarredPaper(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="starred_papers"
    )
    paper = models.ForeignKey(
        ResearchPaper,
        on_delete=models.CASCADE,
        related_name="starred_by"
    )
    starred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "paper")
