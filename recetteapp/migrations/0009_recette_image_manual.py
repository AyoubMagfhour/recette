# Generated by Django 4.2 on 2023-05-03 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetteapp', '0008_favoriterecette'),
    ]

    operations = [
        migrations.AddField(
            model_name='recette',
            name='image_manual',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
