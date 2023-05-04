from django.db import models
from django.contrib.auth.models import User

class Recette(models.Model):
    id_recette = models.AutoField(primary_key=True)
    nom_recette = models.CharField(max_length=100)
    categorie = models.CharField(max_length=50)
    ingredients = models.TextField()
    discription = models.TextField()
    image = models.TextField()
    image_manual = models.TextField(default=None, null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Recette"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, default=1)
    rating = models.IntegerField(default=0)

    class Meta:
        db_table = "Comment"


class FavoriteRecette(models.Model):
    id = models.AutoField(primary_key=True)
    id_recette = models.ForeignKey('Recette', on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite_recette'

