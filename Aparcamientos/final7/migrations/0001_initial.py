# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(default='Null', max_length=100)),
                ('Id_Entidad', models.CharField(default='Null', max_length=10)),
                ('Descripcion', models.TextField(default='Null')),
                ('Accesibilidad', models.IntegerField(default=0)),
                ('Enlace', models.URLField(default='Null')),
                ('Clase_Via', models.CharField(default='Null', max_length=20)),
                ('Nombre_Via', models.CharField(default='Null', max_length=20)),
                ('Numero_Via', models.CharField(default='Null', max_length=10)),
                ('Codigo_Postal', models.CharField(default='Null', max_length=10)),
                ('Barrio', models.CharField(default='Null', max_length=50)),
                ('Distrito', models.CharField(default='Null', max_length=50)),
                ('Latitud', models.CharField(default='Null', max_length=25)),
                ('Longitud', models.CharField(default='Null', max_length=25)),
                ('Telefono', models.CharField(default='Null', max_length=50)),
                ('Email', models.CharField(default='Null', max_length=75)),
                ('Num_Coment', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Texto', models.TextField(default='Null')),
                ('Fecha', models.DateTimeField(auto_now_add=True)),
                ('Aparc_Coment', models.CharField(default='Null', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Pag_Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('Propietario', models.CharField(max_length=20)),
                ('Tit_Pagina', models.CharField(max_length=20)),
                ('Color_Pagina', models.CharField(max_length=20)),
                ('Letra_pagina', models.CharField(max_length=20)),
                ('Aparc_Selec', models.ManyToManyField(to='final7.Aparcamiento')),
            ],
        ),
    ]
