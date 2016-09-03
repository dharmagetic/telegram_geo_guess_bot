# coding: utf8

from django.core.management import BaseCommand

from geo.models import Country


class Command(BaseCommand):
    def _make_country(self, line):
        line.rstrip('\n')
        country = line.split('–')
        country_name = country[0].strip()
        country_capital = country[1].strip()
        Country.objects.create(
            name=country_name,
            capital=country_capital
        )

    def handle(self, *args, **options):
        Country.objects.all().delete()
        with open('countries_capitals.txt', 'r') as f:
            for line in f:
                self._make_country(line)