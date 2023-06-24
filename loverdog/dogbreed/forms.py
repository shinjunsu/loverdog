from django import forms

class DogImageUploadForm(forms.Form):
    image = forms.ImageField(label='Upload a dog image')
