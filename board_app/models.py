from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Card(models.Model):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=False, max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='card', default=1)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
