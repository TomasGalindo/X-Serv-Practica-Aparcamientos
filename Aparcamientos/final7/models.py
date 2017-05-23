from django.db import models
# Create your models here.


class Aparcamiento(models.Model):
    Nombre = models.CharField(max_length=100, default="Null")
    Id_Entidad = models.CharField(max_length=10, default="Null")
    Descripcion = models.TextField(default="Null")
    Accesibilidad = models.IntegerField(default=0)
    Enlace = models.URLField(default="Null")
    # Datos Direccion
    Clase_Via = models.CharField(max_length=20, default="Null")
    Nombre_Via = models.CharField(max_length=20, default="Null")
    Numero_Via = models.CharField(max_length=10, default="Null")
    Codigo_Postal = models.CharField(max_length=10, default="Null")
    Barrio = models.CharField(max_length=50, default="Null")
    Distrito = models.CharField(max_length=50, default="Null")
    Latitud = models.CharField(max_length=25, default="Null")
    Longitud = models.CharField(max_length=25, default="Null")
    # datos de contacto
    Telefono = models.CharField(max_length=50, default="Null")
    Email = models.CharField(max_length=75, default="Null")
    Num_Coment = models.IntegerField(default=0)


class Comentario(models.Model):
    Texto = models.TextField(default="Null")
    Fecha = models.DateTimeField(auto_now_add=True)
    # IdEntidad de aparcamiento
    Aparc_Coment = models.CharField(max_length=10, default="Null")


class Pag_Usuario(models.Model):
    Propietario = models.CharField(max_length=20)
    Tit_Pagina = models.CharField(max_length=20)
    Color_Pagina = models.CharField(max_length=20, default="white")
    Letra_pagina = models.CharField(max_length=20, default="90%")
    Aparc_Selec = models.ManyToManyField(Aparcamiento)
