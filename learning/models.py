from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def total_topics_count(self):
        return self.topics.count()

    @property
    def completed_topics_count(self):
        return self.topics.filter(status='COMPLETED').count()

    @property
    def progress_percentage(self):
        total = self.total_topics_count
        if total == 0:
            return 0
        return int(round((self.completed_topics_count / total) * 100))


class Topic(models.Model):
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('CURRENTLY_LEARNING', 'Currently Learning'),
        ('COMPLETED', 'Completed'),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    date_learned = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.order:02d} — {self.title}"
