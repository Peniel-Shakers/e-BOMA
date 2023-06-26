"""eBOMA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from boutique.views import *
from comptes.views import *
from eBOMA import settings

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion_user, name="connexion"),
    path('deconnexion/', deconnexion_user, name="deconnexion"),
    path('panier/', panier, name="panier"),
    path('panier/supprimer', supprimer_panier, name="supprimer-panier"),
    path('panier/valider', valider_panier, name="valider-panier"),
    path('deconnexion/', deconnexion_user, name="deconnexion"),
    path('fromage/<str:slug>/', fromage_details, name="fromage"),
    path('fromage/<str:slug>/ajouter-au-panier/ ', ajouter_au_panier, name="ajouter-au-panier"),
    path('paiement/', PaymentView.as_view(), name='paiement'),
    path('facture/', valider_panier, name='facture'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
