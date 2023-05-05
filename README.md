# recette
<h2>Note :</h2>
<ul>
  <li>Avant l'execution du projet il faut créer un super utilisateur avec la commande "python manage.py createsuperuser"</li>
  <li>Executer et accédé à "/admin"</li>
  <li>Apres créer 2 groupes Ban et visiteur </li>
  <li>connecter à votre compte est créér 2 groupes 'Ban' et 'visiteur'</li>
  <li>Visiteur contient les Permissions Suivantes :</li>
  <ul>
    <li>can add comment</li>
    <li>can delete favorite recette</li>
    <li>can view favorite recette</li>
    <li>can add recette</li>
    <li>can view recette</li>
   </ul>
</ul>


<h2>Les Fonctions qu'on a utilisé dans ce projet :</h2>

<h4>Login_view :</h4>
<p>Ce code gère l'authentification des utilisateurs sur le site web. Il vérifie si la méthode de
requête HTTP est POST, récupère le nom d'utilisateur et le mot de passe soumis dans le
formulaire de connexion, puis utilise la fonction authenticate pour valider les informations
d'identification de l'utilisateur. Si les informations d'identification sont valides, l'utilisateur
est connecté en utilisant la fonction login. La vue vérifie ensuite si l'utilisateur appartient
au groupe "visiteur" et le redirige vers la page "listrecette" s'il en fait partie, ou vers la page
"login" s'il appartient au groupe "ban". Si l'utilisateur n'appartient à aucun de ces groupes, il
est redirigé vers la page "dashboard". Si les informations d'identification ne sont pas valides,
l'utilisateur est renvoyé à la page de connexion avec un message d'erreur.</p>

<h4>Sign-up :</h4>
<p>ce code traite les inscriptions de nouveaux utilisateurs sur le site web. Si la méthode de
requête HTTP est POST, la vue récupère les informations d'inscription soumises dans le
formulaire de création de compte. Elle vérifie que les mots de passe saisis correspondent et
qu'un utilisateur avec le même nom d'utilisateur n'existe pas déjà. Si les conditions sont
remplies, la vue crée un nouvel utilisateur en utilisant les informations soumises dans le
formulaire et l'ajoute au groupe "visiteur". Ensuite, elle authentifie et connecte
automatiquement le nouvel utilisateur en utilisant la fonction login, et le redirige vers la
page de connexion.
</p>

<h4>Logout :</h4>
<p>ce code gère la déconnexion des utilisateurs sur le site web. Lorsque la vue est appelée, elle
utilise la fonction logout pour déconnecter l'utilisateur en cours et redirige
automatiquement vers la page "listrecette".
</p>

<h4>Add_recette:</h4>
<p>ce code permet d'ajouter une nouvelle recette au site web. La vue nécessite que l'utilisateur
soit connecté et qu'il soit un superutilisateur pour pouvoir accéder à la page d'ajout de
recette. La vue permet à l'utilisateur de saisir les détails de la recette, tels que le titre, la
catégorie, les ingrédients et la description, et de télécharger une image de la recette. La vue
encode l'image en base64 et la sauvegarde en tant que champ d'image de la recette.
Ensuite, la vue redirige l'utilisateur vers la page de liste des recettes. Si la requête HTTP n'est
pas de type POST, la vue affiche la page d'affichage des recettes.</p>


<h4>Extract_data :</h4>
<p>Cette fonction prend en entrée le contenu HTML d'une page et l'URL de base, et renvoie
une liste d'objets contenant les informations sur les images de la page.
La fonction parcourt le contenu HTML avec BeautifulSoup et cherche tous les éléments
ayant un attribut style contenant la chaîne "background-image". Elle extrait l'URL de
l'image à partir de cet attribut et cherche ensuite l'élément figcaption correspondant
pour obtenir la légende. Si disponible, elle cherche également le lien hypertexte vers la
recette en cherchant l'élément parent figure avec la classe m-fig.</p>

<h4>Affiche :</h4>
<p>ce code affiche une liste de recettes aléatoires de cuisine à partir du site Journal des
Femmes. Elle nécessite que l'utilisateur soit connecté et soit un super-utilisateur pour être
accessible.
La fonction commence par générer deux nombres aléatoires entre 1 et 10, et utilise ces
nombres pour sélectionner une plage de pages à partir du site Journal des Femmes. Ensuite,
pour chaque page sélectionnée, la fonction utilise une fonction auxiliaire appelée
extract_data pour extraire les données pertinentes, telles que le titre, la description, les
ingrédients et l'image de chaque recette.
Enfin, toutes les données sont stockées dans une liste data_list et renvoyées au modèle
pour être affichées.</p>

<h4>Middleware function :</h4>
<p>Un middleware est une fonction qui peut être utilisée pour effectuer une action sur chaque
requête entrante ou sortante d'une application Django.
Dans ce middleware, la fonction __call__ est appelée à chaque fois qu'une requête est
reçue par l'application. Si la requête correspond à la page d'accueil (/index/), le nombre
d'accès à la page de tableau de bord est récupéré à partir de la session de l'utilisateur et
incrémenté de 1. La nouvelle valeur est ensuite stockée dans la session.</p>

<h4>Search :</h4>
<p>cette fonction une vue de recherche de recettes qui permet de filtrer les recettes par nom
ou par catégorie. Les paramètres de recherche sont obtenus à partir de la requête GET
search et category.
La vue utilise un queryset de toutes les recettes. Si la recherche est effectuée, elle est
filtrée par nom de recette en utilisant la méthode icontains. Si la catégorie est
sélectionnée, la requête est filtrée par catégorie en utilisant la méthode iexact.
Ensuite, la vue utilise un objet Paginator pour afficher les recettes paginées. Si la requête
est une requête POST, cela signifie qu'un utilisateur a cliqué sur le bouton "Ajouter aux
favoris" d'une recette. Si l'utilisateur est authentifié, une nouvelle entrée de
FavoriteRecette est créée pour l'utilisateur connecté et la recette en question. Si
l'utilisateur n'est pas authentifié, il est redirigé vers la page de connexion.
Enfin, la vue renvoie le rendu de la page HTML visiteur/search.html, avec les résultats
de la recherche paginés, ainsi que la liste des utilisateurs ayant créé les recettes affichées.
</p>

<h4>Dashboard :</h4>
<p>Cette fonction implémente une vue pour le tableau de bord d'une application. Elle utilise
différentes requêtes pour récupérer des données sur les recettes, les utilisateurs, et les
connexions récentes. Plus précisément, elle:
<ul>
  <li>Utilise la méthode annotate pour calculer la note moyenne Etoile pour chaque
  recette, et order_by pour récupérer la recette la mieux notée.</li>
  <li>Utilise la méthode count pour récupérer le nombre total de recettes</li>
  <li>Récupère un groupe d'utilisateurs spécifique (dans ce cas, "visiteur") à partir de son
  nom, puis compte le nombre d'utilisateurs qui en font partie.</li>
  <li>Utilise la date actuelle pour récupérer les nouveaux utilisateurs qui ont rejoint le
  groupe "visiteur" depuis aujourd'hui.</li>
  <li>Utilise l'attribut session de l'objet de requête pour récupérer le nombre d'accès au
  tableau de bord.</li>
</ul>
</p>

<h4>Recette_Detail :</h4>
<p>Cette fonction prend en entrée un objet requête "request" et une variable "pk" qui
représente l'identifiant d'une recette dans la base de données. La fonction utilise la fonction
"get_object_or_404" pour récupérer l'objet "Recette" correspondant à l'identifiant "pk"
dans la base de données. Ensuite, la fonction divise les ingrédients et les descriptions en
listes en utilisant la méthode "split" de Python. Enfin, la fonction récupère tous les
commentaires associés à la recette et renvoie une réponse HTTP avec un contexte
contenant les informations sur la recette, les commentaires, les ingrédients, les
descriptions, les utilisateurs et 8 recettes aléatoires.</p>
