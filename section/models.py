from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey(User, null=True, default=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Title(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Classification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
