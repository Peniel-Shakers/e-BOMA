from email.policy import default
from django.db import models
from django.urls import reverse
from django.utils import timezone
from eBOMA.settings import AUTH_USER_MODEL

# Create your models here.


class Fromage(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="fromages", blank=True, null=True)
    slug = models.SlugField(max_length=128)
    
    def __str__(self):
        return f"{self.nom} ({self.stock}) : {self.prix}$"
    
    def get_absolute_url(self):
        return reverse("fromage", kwargs={"slug": self.slug})
    

class Facture(models.Model):
    utilisateur = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(blank=True, default=timezone.now())
    montant_total = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.utilisateur.username} | Montant total: {self.montant_total}$ | Date de commande : {self.date_commande}"


class Commande(models.Model):
    utilisateur = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    fromage = models.ForeignKey(Fromage, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    validation = models.BooleanField(default=False)
    montant = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    date_commande = models.DateTimeField(blank=True, default=timezone.now())
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.fromage.nom} ({self.quantite}) : {self.fromage.prix * self.quantite}$"

    def calculer_montant(self):
        self.montant = self.fromage.prix * self.quantite
        self.save()

class Panier(models.Model):
    utilisateur = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    commandes = models.ManyToManyField(Commande)

    def __str__(self):
        return f"{self.utilisateur.username} "

    def delete(self, *args, **kwargs):
        for commande in self.commandes.all():
            commande.validation = True
            commande.date_commande = timezone.now()
            commande.save()

        self.commandes.clear()
        super().delete(*args, **kwargs)

    def calculer_total(self):
        total = 0
        for commande in self.commandes.all():
            commande.calculer_montant()
            total += commande.montant
        return total
