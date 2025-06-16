from django.db import models
from django.contrib.auth.models import User

# Modello per estendere il profilo utente standard di Django
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link al modello User di Django

    # Campi anagrafici aggiuntivi
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    data_nascita = models.DateField()
    codice_fiscale = models.CharField(max_length=16, unique=True)
    telefono = models.CharField(max_length=15)

    # Campi relativi alle funzionalità dell'applicazione
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notifiche_attive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome} {self.cognome}" # Rappresentazione testuale dell'oggetto
    
# Modello per le notifiche utente
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Utente a cui è destinata la notifica
    message = models.TextField() # Contenuto della notifica
    is_read = models.BooleanField(default=False) # Stato di lettura della notifica
    created_at = models.DateTimeField(auto_now_add=True) # Data e ora di creazione