from django.db import models

class DogBreed(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dog_images/')

    def __str__(self):
        return self.name



class DogBreedPrediction(models.Model):
    image = models.ImageField(upload_to='dog_images/', null=True, blank=True)
    predicted_breed = models.CharField(max_length=100, default='Unknown')

    def __str__(self):
        return self.predicted_breed