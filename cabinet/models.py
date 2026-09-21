from django.db import models

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    date_naissance = models.DateField()

    def __str__(self):
        return self.nom + " " + self.prenom


class Dentiste(models.Model):
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom


class Rendezvous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentiste = models.ForeignKey(Dentiste, on_delete=models.CASCADE)
    date = models.DateField()
    heure = models.TimeField()
    motif = models.TextField()
    statut = models.CharField(max_length=50, default="En attente")

    def __str__(self):
        return f"{self.patient} avec {self.dentiste} le {self.date}"
    
class Recu(models.Model):
    rendezvous    = models.OneToOneField(Rendezvous, on_delete=models.CASCADE)
    montant       = models.DecimalField(max_digits=8, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=50, choices=[
        ('especes', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement'),
    ], default='especes')

    def __str__(self):
        return f"Reçu #{self.id} - {self.rendezvous.patient}"