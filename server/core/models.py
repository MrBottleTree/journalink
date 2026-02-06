from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ResearchPaper(models.Model):
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    journal_name = models.CharField(max_length=255)
    published_date = models.DateTimeField()
    file_url = models.URLField()

    # Relations from ER Diagram
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="papers")
    topics = models.ManyToManyField(Topic, related_name="papers")
    citations = models.ManyToManyField('self', symmetrical=False, related_name='cited_by', blank=True)

    def __str__(self):
        return self.title