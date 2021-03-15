from django.db import models


# Create your models here.

# class ->UserProfile
# 表名 user_profile
# user_nam,nick_name,email,password,sign,info,avatar

class UserProfile(models.Model):
    username = models.CharField(max_length=11, verbose_name="用戶名", primary_key=True)
    nickname = models.CharField(max_length=30, verbose_name="匿名")
    email = models.CharField(max_length=50, verbose_name="電子郵箱", null=True)
    password = models.CharField(max_length=32)
    sign = models.CharField(max_length=50, verbose_name="個人簽名")
    info = models.CharField(max_length=150, verbose_name="個人描述")
    avatar = models.ImageField(upload_to='avatar/')
    score = models.IntegerField(verbose_name="分數", null=True, default=0)

    class Meta:
        """
            更改表明
        """
        db_table = "user_profile"
