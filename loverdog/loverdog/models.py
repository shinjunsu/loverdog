from django.db import models
from django.conf import settings
from .management.commands.train_model import train_and_save_model

class DogBreedPrediction(models.Model):
    image = models.ImageField(upload_to='dog_images/')
    predicted_breed = models.CharField(max_length=100)

    def __str__(self):
        return self.predicted_breed

class DogBreed(models.Model):
    # Your dog breed model fields

    @staticmethod
    def train_model():
        trained_model_path = settings.TRAINED_MODEL_PATH
        train_and_save_model(trained_model_path)
