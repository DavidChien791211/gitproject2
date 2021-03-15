from django.db import models
from user.models import UserProfile

# Create your models here.
class Image(models.Model):
    img = models.ImageField(upload_to='upload/')
    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile)
    class Meta:
        db_table = "user_picture"