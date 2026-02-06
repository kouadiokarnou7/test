from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
 
# Create your views here.

def landing_page(request):
    return render(request, 'index.html') 


def register_page(request):
    if request.method == "POST":
        # On récupère les données du formulaire Tailwind (attributs 'name')
        fullname = request.POST.get('nom_complet')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')
        # 1. Vérification des mots de passe
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'register.html')

        # 2. Vérification si l'email existe déjà
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, 'register.html')

        # 3. Création de l'utilisateur
        # On utilise l'email comme 'username' car Django en a besoin d'un unique
        user = User.objects.create_user(username=email, email=email, password=password)
        
        # On sépare le nom complet en prénom/nom pour Django
        if " " in fullname:
            user.first_name, user.last_name = fullname.split(" ", 1)
        else:
            user.first_name = fullname
        
        user.save()
        
        # 4. Connexion automatique et redirection
        login(request, user)
        return redirect('home')
    return render(request,'authentification/register.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # On cherche l'utilisateur par son email (qui est aussi son username ici)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email ou mot de passe invalide.")
    return render(request,'authentification/login.html')


def logout_page(request):
    logout(request)
    return redirect('login')


def reset_page(request):
    return render(request,'authentification/reset.html')    