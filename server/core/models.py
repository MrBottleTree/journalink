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

    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Defines if the project is under SOP, DOP, LOP
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Informal')
    
    # include slots and prereqs that students might need 
    prerequisites = models.TextField(help_text="e.g. 'Must know Python. Min CGPA 7.0'")
    slots_available = models.IntegerField(default=3)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.project_type})"

# The relationship for student and project should in the student 


class ProjectApplication(models.Model):
    STATUS_CHOICES = [
        ('Interested', 'Interested'),
        ('Shortlisted', 'Shortlisted'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    # the foreign keys => which student is applying for and what project 
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Student details that might be needed for project like resume, cgpa 
    student_cgpa = models.DecimalField(max_digits=4, decimal_places=2, help_text="Current CGPA")
    cover_letter = models.TextField(help_text="Why are you a good fit for this project?")
    resume_link = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Interested')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.project.title}"