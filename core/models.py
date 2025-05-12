from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    data_nascita = models.DateField()
    codice_fiscale = models.CharField(max_length=16, unique=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nome} {self.cognome}"