import datetime
import os
import random

import base64
import uuid

from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.http import HttpResponse, response
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm
from .models import Recette, Comment, FavoriteRecette
from .utils import extract_data
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'visiteur/index.html')

def recipe(request):
    return render(request, 'visiteur/recipe.html')


def search(request):
    queryset = Recette.objects.all()
    search_query = request.GET.get('search')
    category = request.GET.get('category')

    if search_query:
        queryset = queryset.filter(nom_recette__icontains=search_query)

    if category:
        queryset = queryset.filter(categorie__iexact=category)

    paginator = Paginator(queryset, 16)
    page = request.GET.get('page', 1)

    try:
        recette = paginator.page(page)
    except PageNotAnInteger:
        recette = paginator.page(1)
    except EmptyPage:
        recette = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        if request.user.is_authenticated:
            recette_id = request.POST.get('recette_id')
            recette = get_object_or_404(Recette, pk=recette_id)
            favorite_recette = FavoriteRecette.objects.create(id_recette=recette, id_user=request.user)
            favorite_recette.save()
            return redirect('search')
        else:
            return redirect('login')

    users = [recette.id_user for recette in recette]
    return render(request, 'visiteur/search.html', {'recettes': recette, 'users': users})

def contact(request):
    return render(request, 'visiteur/contact.html')

def register(request):
    return render(request, 'visiteur/sign-up.html')

def connexion(request):
    return render(request, 'visiteur/sign-in.html')


@login_required(login_url='/login')
def ban(request):
    return render(request, 'ban.html')

@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    highest_rated_recette = Recette.objects.annotate(avg_rating=Avg('comment__rating')).order_by('-avg_rating').first()
    num_recettes = Recette.objects.count()
    visiteur_group = Group.objects.get(name='visiteur')
    num_visiteur_users = visiteur_group.user_set.count()
    today = datetime.date.today()
    new_users = visiteur_group.user_set.filter(date_joined__gte=today)
    access_count = request.session.get('dashboard_access_count', 0)
    context = {
        'highest_rated_recette': highest_rated_recette,
        'num_recettes': num_recettes,
        'num_visiteur_users': num_visiteur_users,
        'new_users': new_users,
        'access_count': access_count,
    }
    return render(request, 'page2/dashboard.html', context)

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def historique(request):
    comments = Comment.objects.all()
    return render(request, 'page2/Historique.html', {'comments': comments})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def suggesion(request):
    return render(request, 'page/page2.html')

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def affiche(request):
    random_range1 = random.randrange(1, 10)
    random_range2 = random.randrange(random_range1 + 1, 11)
    base_url = "https://cuisine.journaldesfemmes.fr"
    page_urls = [base_url + "/recette-aperitif-buffet/preferes-page{}".format(i) for i in range(random_range1, random_range2)]
    data_list = []
    for page_url in page_urls:
        response = requests.get(page_url)
        html_content = response.content
        data_list.extend(extract_data(html_content, base_url))

    context = {
        'data_list': data_list
    }

    return render(request, 'page2/Nouvelle.html', context)


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def scrape_view(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        div_element = soup.find('h1', {'class': 'app_recipe_title_page'})
        dsc = soup.find('ol')
        img_url = soup.find('img', {'class': 'bu_cuisine_img_noborder photo'})['src']
        image = img_url
        title = div_element.text.strip()
        description = dsc.text.strip()
        ingredients_ul = soup.find('ul', {'class': 'bu_cuisine_ingredients'})
        if ingredients_ul:
            ingredient_list = []
            for ingredient in ingredients_ul.find_all('li'):
                ingredient_list.append(ingredient.text.strip())
        else:
            ingredients_span = soup.find_all('span', {'class': 'jHiddenHref'})
            if ingredients_span:
                ingredient_list = []
                for ingredient in ingredients_span:
                    ingredient_list.append(ingredient.text.strip())
            else:
                ingredient_list = []

        return render(request, 'page2/Scraping.html', {'title': title, 'image': image, 'description': description, 'ingredient': ingredient_list})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def add_recette(request):
    categorie_map = {
        '1': 'Entrées',
        '2': 'Plats',
        '3': 'Desserts'
    }
    if request.method == 'POST':
        nom_recette = request.POST.get('title')
        categorie = categorie_map.get(request.POST.get('categorie'))
        ingredients = request.POST.get('ingredient')
        description = request.POST.get('description')
        image_manual = request.FILES['image_manual']
        id_user = request.user

        if image_manual :
            image_data = image_manual.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            data_url = f"data:image/{os.path.splitext(image_manual.name)[1][1:]};base64,{base64_data}"
            recette = Recette(nom_recette=nom_recette, categorie=categorie, ingredients=ingredients,
                              discription=description, image_manual=data_url, id_user=id_user)
            recette.save()

        return redirect('/recette')

    return render(request, '/affiche')

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def add_recette2(request):
    categorie_map = {
        '1': 'Entrées',
        '2': 'Plats',
        '3': 'Desserts'
    }
    if request.method == 'POST':
        nom_recette = request.POST.get('title')
        categorie = categorie_map.get(request.POST.get('categorie'))
        ingredients = request.POST.get('ingredient')
        description = request.POST.get('description')
        image = request.POST.get('image')
        id_user = request.user

        recette = Recette(nom_recette=nom_recette, categorie=categorie, ingredients=ingredients,
                              discription=description, image=image, id_user=id_user)

        recette.save()

        return redirect('/recette')
    return render(request, '/affiche')

def logout_view(request):
    logout(request)
    return redirect('listrecette')


def sign_up(request):
    if request.method == 'POST':
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'registration/sign-up.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'registration/sign-up.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name,
                                        last_name=last_name)

        visitor_group = Group.objects.get(name='visiteur')
        visitor_group.user_set.add(user)

        user = authenticate(username=username, password=password1)
        login(request, user)
        return redirect('login')

    return render(request, 'registration/sign-up.html')

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def all_recette(request):
    recette = Recette.objects.all()
    return render(request, 'page2/recette.html', {'recettes': recette})

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def delete_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    recette.delete()
    return redirect('/recette')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='visiteur').exists():
                return redirect('listrecette')
            elif user.groups.filter(name='ban').exists():
                return redirect('login')
            else:
                return redirect('dashboard')
        else:
            error_message = "Invalid username or password."
            return render(request, 'registration/sign-in.html', {'error_message': error_message})
    else:
        return render(request, 'registration/sign-in.html')


@login_required(login_url='/login')
def add_comment(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    if request.method == 'POST':
        message = request.POST.get('comment')
        user = request.user
        rating = request.POST.get('rating')
        comment = Comment(message=message, user=user, recette=recette, rating=rating, date_sent=timezone.now())
        comment.save()
        return redirect('recipe_detail', pk=pk)
    else:
        return redirect('recipe_detail', pk=pk)



@login_required(login_url='/login')
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('/historique')



def allrecettevisiteur(request):
    queryset = Recette.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(nom_recette__icontains=search_query)
    paginator = Paginator(queryset, 12)
    page = request.GET.get('page', 1)
    try:
        recette = paginator.page(page)
    except PageNotAnInteger:
        recette = paginator.page(1)
    except EmptyPage:
        recette = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        if request.user.is_authenticated:
            recette_id = request.POST.get('recette_id')
            recette = get_object_or_404(Recette, pk=recette_id)
            favorite_recette = FavoriteRecette.objects.create(id_recette=recette, id_user=request.user)
            favorite_recette.save()
            return redirect('listrecette')
        else:
            return redirect('login')
    users = [recette.id_user for recette in recette]
    return render(request, 'visiteur/index.html', {'recettes': recette, 'users': users })




def recipe_detail(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    ingredients = recette.ingredients.split('\n') if recette.ingredients else []
    descriptions = recette.discription.split('\n') if recette.discription else []
    comments = recette.comment_set.all()
    recettes = Recette.objects.order_by('?')[:8]
    random.shuffle(list(recettes))
    context = {'recette': recette, 'pk': pk, 'comments': comments, 'ingredients': ingredients, 'descriptions': descriptions, 'users': recette.id_user, 'recettes': recettes}
    return render(request, 'visiteur/recipe.html', context)

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def users_list(request):
    visiteurs_group = Group.objects.get(name='visiteur')
    visiteurs = visiteurs_group.user_set.all()
    context = {'visiteurs': visiteurs}
    return render(request, 'page2/Utilisateur.html', context)

@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def ban_visitor(request, pk):
    visiteur = get_object_or_404(User, pk=pk)
    visiteur.groups.clear()
    ban_group = Group.objects.get(name='ban')
    ban_group.user_set.add(visiteur)
    return redirect('visiteur')

@login_required(login_url='/login')
def favorite_recettes(request):
    favorite_recettes = FavoriteRecette.objects.filter(id_user=request.user)
    paginator = Paginator(favorite_recettes, 16)
    page = request.GET.get('page', 1)
    try:
        favorite_recettes = paginator.page(page)
    except PageNotAnInteger:
        favorite_recettes = paginator.page(1)
    except EmptyPage:
        favorite_recettes = paginator.page(paginator.num_pages)

    users = [recette.id_user for recette in favorite_recettes]
    return render(request, 'visiteur/Favorite.html', {'favorite_recettes': favorite_recettes, 'users': users})


@login_required(login_url='/login')
def add_recetteclient(request):
    categorie_map = {
        '1': 'Entrées',
        '2': 'Plats',
        '3': 'Desserts'
    }
    if request.method == 'POST':
        nom_recette = request.POST.get('title')
        categorie = categorie_map.get(request.POST.get('categorie'))
        ingredients = request.POST.get('ingredient')
        description = request.POST.get('description')
        image_manual = request.FILES['image_manual']
        id_user = request.user

        if image_manual :
            image_data = image_manual.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            data_url = f"data:image/{os.path.splitext(image_manual.name)[1][1:]};base64,{base64_data}"
            recette = Recette(nom_recette=nom_recette, categorie=categorie, ingredients=ingredients,
                              discription=description, image_manual=data_url, id_user=id_user)
            recette.save()

        return redirect('/index')

    return render(request, '/contact')






#test admin view
def adminform(request):
    return render(request, 'page2/Formulaire.html')


def delete_fav(request, pk):
    favorite = get_object_or_404(FavoriteRecette, pk=pk)
    if favorite.id_user == request.user:
        favorite.delete()
    return redirect('/favorite')


def adminlogin(request):
    return render(request, 'page2/sign-in.html')

def adminsign(request):
    return render(request, 'page2/sign-up.html')


def edit_recette(request, pk):
    recette = get_object_or_404(Recette, pk=pk)
    context = {'recette': recette}
    return render(request, 'page2/UpdateRecette.html', context)


def update_recette(request, pk):
    categorie_map = {
        '1': 'Entrées',
        '2': 'Plats',
        '3': 'Desserts'
    }
    recette = Recette.objects.get(pk=pk)
    if request.method == 'POST':
        recette.nom_recette = request.POST.get('title')
        recette.categorie = categorie_map.get(request.POST.get('categorie'))
        recette.ingredients = request.POST.get('ingredient')
        recette.discription = request.POST.get('description')
        recette.save()

        return redirect('/recette')
    else:
        return render(request, 'update_recette.html', {'recette': recette})