# Generated by Django 3.2.19 on 2023-06-07 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
