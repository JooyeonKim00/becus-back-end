from django.db import models


# Create your models here.
class Product(models.Model):
    p_number = models.CharField(max_length=30)
    p_name = models.CharField(max_length=30)
    p_content = models.TextField()
    p_picture = models.URLField(max_length=200)
    p_video = models.URLField(max_length=200)
    p_manual = models.URLField(max_length=200)
    p_author = models.ForeignKey('user.User', on_delete=models.CASCADE)