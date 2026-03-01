from django.db import models
from django.contrib.auth.models import User

class USER(models.Model):
    class Choices(models.TextChoices):
        STUDENT = 'Student', 'Student'
        PROFESSOR = 'Professor', 'Professor'
        
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=Choices.choices)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class POST(models.Model):

    class CategoryChoices(models.TextChoices):
        ACADEMIC = 'Academic', 'Academic'
        GENERAL = 'General', 'General'
        
    post_id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=300)  
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class PROJECT(models.Model):

    class Status(models.TextChoices):
        PROPOSED = 'Proposed', 'Proposed'
        ON_GOING = 'On Going', 'On Going'
        COMPLETED = 'Completed', 'Completed'

    project_id = models.IntegerField(primary_key=True)
    professor = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ON_GOING)

class PROJECT_APPLICATION(models.Model):
    
    class Status(models.TextChoices):
        REJECTED = 'Rejected', 'Rejected'
        ACCEPTED = 'Accepted', 'Accepted'
        WAITING = 'Waiting', 'Waiting'

    proj_app_id = models.IntegerField(primary_key=True)
    project = models.ForeignKey(PROJECT, on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="project_applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.WAITING)

class POST_TAGS(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(POST, on_delete=models.CASCADE, related_name="tags")
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="tags_in_posts")
