# Generated by Django 3.2.19 on 2023-06-24 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogbreed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogbreedprediction',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dog_images/'),
        ),
        migrations.AddField(
            model_name='dogbreedprediction',
            name='predicted_breed',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
