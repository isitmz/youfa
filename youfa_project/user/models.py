from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Campi aggiuntivi associato a quell'id user
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    data_nascita = models.DateField()
    codice_fiscale = models.CharField(max_length=16, unique=True)
    telefono = models.CharField(max_length=15)

    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notifiche_attive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.cognome}"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)