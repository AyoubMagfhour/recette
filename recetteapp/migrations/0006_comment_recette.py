# Generated by Django 4.2 on 2023-04-29 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recetteapp', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='recette',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recetteapp.recette'),
        ),
    ]
