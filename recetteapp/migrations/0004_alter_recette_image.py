# Generated by Django 4.2 on 2023-04-26 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetteapp', '0003_alter_recette_id_recette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='image',
            field=models.TextField(),
        ),
    ]
