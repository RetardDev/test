# Generated by Django 5.0 on 2023-12-28 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_services_serviceimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='services_offered',
            field=models.ManyToManyField(to='store.services'),
        ),
    ]
