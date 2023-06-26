# Generated by Django 4.1.7 on 2023-04-25 03:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boutique', '0006_remove_panier_date_commande_remove_panier_validation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='date_commande',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 25, 3, 18, 2, 595250, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(blank=True, default=datetime.datetime(2023, 4, 25, 3, 18, 2, 595250, tzinfo=datetime.timezone.utc))),
                ('montant_total', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]