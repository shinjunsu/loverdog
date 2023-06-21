from django.db import models

# Create your models here.

class dogImg(models.Model):
    image = models.ImageField(upload_to='dog_images/')

class analysis_result(models.Model):
    dogImg = models.ForeignKey(dogImg,on_delete=models.CASCADE)
    result = models.TextField()
