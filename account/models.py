from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from staff.models import Employee


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    staff_profile = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    immediate_supervisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="immediate_supervisor")
    is_supervisor = models.BooleanField(default=False, null=True, blank=True)
    is_hod = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.image.path)
