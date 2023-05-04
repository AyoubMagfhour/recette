from django.urls import path
from .views import *

urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
    path('recette/', all_recette, name='recette'),
    path('historique/', historique, name='historique'),
    path('visiteur/', users_list, name='visiteur'),
    path('suggesion/', suggesion, name='suggesion'),
    path('affiche/', affiche, name='affiche'),
    path('scrape/', scrape_view, name='scrape'),
    path('add_recette/', add_recette, name='add_recette'),
    path('add_recette2/', add_recette2, name='add_recette2'),
    path('logout/', logout_view, name='logout'),
    path('sign-up', sign_up, name='sign_up'),
    path('delete/<int:pk>/', delete_recette, name='delete_recette'),
    path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),
    path('login/', login_view, name='login'),
    path('add_comment/<int:pk>/', add_comment, name='add_comment'),
    path('ban_visitor/<int:pk>/', ban_visitor, name='ban_visitor'),


    ##visiteur
    path('index/', allrecettevisiteur, name='listrecette'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('search/', search, name='search'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('connexion/', connexion, name='connexion'),
    path('favorite/', favorite_recettes, name='favorite'),
    path('add_recetteclient/', add_recetteclient, name='add_recetteclient'),
    path('delete_fav/<int:pk>/', delete_fav, name='delete_fav'),


    #admin test
    path('formnv/', adminform, name='formnv'),
    path('L2/', adminsign, name='L2'),
    path('edit_recette/<int:pk>/', edit_recette, name='edit_recette'),
    path('update_recette/<int:pk>/', update_recette, name='update_recette'),


]