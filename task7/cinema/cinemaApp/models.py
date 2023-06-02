from django.db import models
from django.db.models import F
from django.conf import settings

# Create your models here.
class Projection(models.Model):
    imeFilma = models.CharField(max_length=40, null=True)
    vrijemeFilma = models.DateField(null=True)
    kapacitetDvorane = models.IntegerField(default=0)
    available_seats = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        self.available_seats = self.kapacitetDvorane
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.imeFilma}"



class Ticket(models.Model):
    brojSjedala = models.IntegerField(null=True)
    idKorisnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    idProjekcija = models.ForeignKey(Projection, on_delete =models.CASCADE, null=True)
    def __str__(self):
        return f"Korisnik: {self.idKorisnik} film: {self.idProjekcija}"