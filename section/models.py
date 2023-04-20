from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)

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
