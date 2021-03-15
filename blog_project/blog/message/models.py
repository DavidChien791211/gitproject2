from django.db import models
from user.models import UserProfile
from topic.models import Topic


# Create your models here.
class Message(models.Model):
    conten = models.CharField(max_length=50, verbose_name="內容")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="留言創建時間")
    topic = models.ForeignKey(Topic)
    publisher = models.ForeignKey(UserProfile)
    parent_message = models.IntegerField(default=0)

    class Meta:
        db_table = "message"
