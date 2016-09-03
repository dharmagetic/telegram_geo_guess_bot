# coding: utf8

from __future__ import unicode_literals

from django.db import models


class Country(models.Model):
    name = models.CharField(verbose_name=u"Cтрана", max_length=255, db_index=True)
    capital = models.CharField(verbose_name=u"Столица", max_length=255, db_index=True)

    def __unicode__(self):
        return u"%s – %s" % (self.name, self.capital)