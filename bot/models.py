# coding: utf8

from __future__ import unicode_literals

from random import randint

from django.db import models
from django.db.models.aggregates import Count
from django.db.models.manager import Manager


class RandomGeoObjectManager(Manager):
    def _random_geo_object(self):
        count = self.aggregate(count=Count('id')).get('count')
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def country(self):
        geo_object = self._random_geo_object()
        return geo_object.name

    def capital(self):
        geo_object = self._random_geo_object()
        return geo_object.capital

class Country(models.Model):
    name = models.CharField(verbose_name=u"Cтрана", max_length=255, db_index=True)
    capital = models.CharField(verbose_name=u"Столица", max_length=255, db_index=True)
    random = RandomGeoObjectManager()
    objects = models.Manager()

    def __unicode__(self):
        return u"%s – %s" % (self.name, self.capital)