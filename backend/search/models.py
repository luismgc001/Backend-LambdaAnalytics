from django.db import models

# Create your models here.
class Articulo(models.Model):
    nombre = models.CharField(max_length=255)
    imagen = models.URLField()
    precio = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.nombre