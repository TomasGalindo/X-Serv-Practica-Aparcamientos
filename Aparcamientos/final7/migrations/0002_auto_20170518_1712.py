# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final7', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pag_usuario',
            name='Color_Pagina',
            field=models.CharField(max_length=20, default='white'),
        ),
        migrations.AlterField(
            model_name='pag_usuario',
            name='Letra_pagina',
            field=models.CharField(max_length=20, default='90%'),
        ),
    ]
