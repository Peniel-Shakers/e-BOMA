from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required

User = get_user_model()

def inscription(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        adresse = request.POST.get("adresse")
        telephone = request.POST.get("telephone")
        utilisateur = User.objects.create_user(
            username=username,
            password=password,
            adresse=adresse,
            telephone=telephone
        )

        login(request, utilisateur)
        return redirect('index')

    return render(request, 'comptes/inscription.html')

def connexion_user(request):
    if request.method == "POST":
        nom_utilisateur = request.POST.get("username")
        mot_de_passe = request.POST.get("password")

        utilisateur = authenticate(username=nom_utilisateur, password=mot_de_passe)

        if utilisateur:
            login(request, utilisateur)
            return redirect('index')
    return render(request, 'comptes/connexion.html')

@login_required
def deconnexion_user(request):
    logout(request)
    return redirect('index')

def custom_403_view(request, exception=None):
    return render(request, 'comptes/403.html', status=403)

def custom_404_view(request, exception=None):
    return render(request, 'comptes/404.html', status=404)
