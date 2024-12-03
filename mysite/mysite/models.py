from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
class Persona(models.Model):
    #codigo = models.CharField(primary_key=True,max_length=6)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=400)
    telefono = models.CharField(max_length=15)
    correo = models.CharField(max_length=200)
    usuario = models.CharField(max_length=200)
    contrasena = models.CharField(max_length=200)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.nombre

class Mensaje(models.Model):
    #codigo = models.CharField(primary_key=True,max_length=6)
    Mensaje = models.CharField(max_length=2000)
    Key=models.CharField(max_length=200)
    fecha  = models.DateTimeField(default=timezone.now)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.Mensaje