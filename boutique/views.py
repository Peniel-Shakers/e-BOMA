from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import TemplateView
from django.conf import settings
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    fromages = Fromage.objects.all()
    return render(request, 'boutique/index.html', context={"fromages": fromages})
    
def fromage_details(request, slug ):
    fromage = get_object_or_404(Fromage, slug=slug)
    return render(request, 'boutique/details.html', context={"fromage": fromage})
    
@login_required
def ajouter_au_panier(request, slug):
    utilisateur = request.user
    fromage = get_object_or_404(Fromage, slug=slug)
    panier, _ = Panier.objects.get_or_create(utilisateur=utilisateur)
    commande, cree = Commande.objects.get_or_create(utilisateur=utilisateur, fromage=fromage, validation=False)

    if cree:
        panier.commandes.add(commande)
    else:
        commande.quantite += 1
        commande.save()

    return redirect(reverse("fromage", kwargs={"slug":slug}))

@login_required
def panier(request):
    utilisateur = request.user
    panier = get_object_or_404(Panier, utilisateur=utilisateur)
    total = panier.calculer_total()
    return render(request, 'boutique/panier.html', context={"commandes": panier.commandes.all(),"total": total})

@login_required
def supprimer_panier(request):
    panier = request.user.panier
    if panier:
        panier.delete()
    return redirect('index')

@login_required
def valider_panier(request):
    utilisateur = request.user
    panier = get_object_or_404(Panier, utilisateur=utilisateur)
    total = panier.calculer_total()
    facture = Facture.objects.create(
        utilisateur=utilisateur,
        date_commande=timezone.now(),
        montant_total=total
    )

    for commande in panier.commandes.all():
        commande.validation = True
        commande.fromage.stock -= commande.quantite
        commande.date_commande = timezone.now()
        commande.facture = facture
        commande.save()

    panier.commandes.clear()

    return render(request, 'boutique/facture.html', context={"commandes": panier.commandes.all(), "facture": facture})


class PaymentView(TemplateView):
    template_name = "boutique/payment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_public_key"] = settings.STRIPE_PUBLIC_KEY
        return context

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        utilisateur = request.user
        panier = get_object_or_404(Panier, utilisateur=utilisateur)
        total = panier.calculer_total()
        token = request.POST.get('stripeToken')
        description = request.POST.get('description')
        amount = total * 100

        if amount:
            amount = int(amount)
            if amount < 0.5:
                messages.error(request, "Le montant doit être supérieur ou égal à 1.")
                return redirect('paiement')
        else:
            amount = 0

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=description,
                source=token,
            )
            messages.success(request, 'Paiement réussi')
            facture = Facture.objects.create(
                utilisateur=utilisateur,
                date_commande=timezone.now(),
                montant_total=total
            )

            # Marquer les commandes du panier comme validées et les associer à la facture
            for commande in panier.commandes.all():
                commande.validation = True
                commande.fromage.stock -= commande.quantite
                commande.date_commande = timezone.now()
                commande.facture = facture
                commande.save()

            panier.commandes.clear()
            return render(request, 'boutique/facture.html',
                          context={"commandes": panier.commandes.all(), "facture": facture})

        except stripe.error.CardError as e:
            # Afficher un message d'erreur à l'utilisateur
            body = e.json_body
            err = body.get('error', {})
            messages.error(request, f"Erreur lors du traitement du paiement : {err.get('message')}")
            # Rediriger vers la page de paiement pour réessayer
            return redirect('paiement')



































"""

def liste_des_fromages(request):
    fromages = Fromage.objects.all()
    context = {'fromages': fromages}
    return render(request, 'liste_des_fromages.html', context)

def ajouter_au_panier(request, id):
    fromage = Fromage.objects.get(id=id)
    commande, created = Commande.objects.get_or_create(user=request.user, status='en cours')
    ligne_de_commande, created = LigneDeCommande.objects.get_or_create(commande=commande, fromage=fromage)
    ligne_de_commande.quantite += 1
    ligne_de_commande.save()
    messages.success(request, 'Le fromage a été ajouté au panier.')
    return redirect('liste_des_fromages')

def passer_commande(request):
    commande = Commande.objects.filter(user=request.user, status='en cours').first()
    if not commande:
        messages.error(request, 'Il n\'y a pas de commande en cours.')
        return redirect('liste_des_fromages')
    if request.method == 'POST':
        # valider la commande et générer une facture
        commande.status = 'terminé'
        commande.save()
        Facture.objects.create(montant=commande.prix_total(), commande=commande)
        messages.success(request, 'La commande a été passée.')
        return redirect('historique_des_commandes')
    context = {'commande': commande}
    return render(request, 'passer_commande.html', context)
    
"""