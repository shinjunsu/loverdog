# Generated by Django 3.2.19 on 2023-06-21 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=10)),
                ('member_pw', models.CharField(max_length=10)),
                ('image', models.ImageField(blank=True, upload_to='member/images/%Y/%m/%d')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]