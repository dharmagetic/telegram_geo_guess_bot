# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-08 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='C\u0442\u0440\u0430\u043d\u0430')),
                ('capital', models.CharField(max_length=255, verbose_name='\u0421\u0442\u043e\u043b\u0438\u0446\u0430')),
            ],
        ),
    ]