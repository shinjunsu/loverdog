from django.shortcuts import render, redirect
from .forms import DogImageUploadForm
from .models import DogBreedPrediction
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import pandas as pd

def predict_dog_breed(request):
    if request.method == 'POST':
        form = DogImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Load the pre-trained model
            model = tf.keras.applications.MobileNetV2(weights='imagenet')

            # Read and preprocess the uploaded image
            img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
            img = cv2.resize(img, (224, 224))
            img = img / 255.0
            img = np.expand_dims(img, axis=0)

            # Make the prediction
            prediction = model.predict(img)
            predicted_class = np.argmax(prediction[0])

            # Load the breed labels from CSV
            labels_df = pd.read_csv('C:\gb_ksh\python\loverdog\loverdog\_media\dog_images\csv\labels.csv')
            breed_name = labels_df.iloc[predicted_class]['breed']

            # Create a new instance of DogBreedPrediction and set the breed name
            prediction = DogBreedPrediction()
            prediction.image = image
            prediction.predicted_breed = breed_name
            prediction.save()

            return redirect('breed_prediction')
    else:
        form = DogImageUploadForm()
    return render(request, 'dogbreed/predict.html', {'form': form})

def breed_prediction(request):
    predictions = DogBreedPrediction.objects.all()
    return render(request, 'dogbreed/prediction.html', {'predictions': predictions})
