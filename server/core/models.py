from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    
    TYPE_CHOICES = [
        ('SOP', 'Study Oriented Project'),
        ('LOP', 'Lab Oriented Project'),
        ('DOP', 'Design Oriented Project'),
        ('Informal', 'Informal Research (No Credit)'),
    ]

    # The Professor => The user who creates a project 
    professor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_projects'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Academic Details needed for the project 
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='SOP')
    prerequisites = models.TextField(help_text="e.g. 'Must know Python. Min CGPA 7.0'")
    slots_available = models.IntegerField(default=3)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project_type})"


class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ('Interested', 'Interested'),
        ('Shortlisted', 'Shortlisted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    
    # The Student => The user who actually applies for the project 
    student = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='project_applications'
    )
    
    # Student details that might be needed for project like resume, cgpa
    student_cgpa = models.DecimalField(max_digits=4, decimal_places=2, help_text="Current CGPA")
    cover_letter = models.TextField(help_text="Why are you a good fit?")
    resume_link = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Interested')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a student can only apply once to the same project 
        # unique constraint 
        unique_together = ('project', 'student')

    def __str__(self):
        return f"{self.student.username} -> {self.project.title}"