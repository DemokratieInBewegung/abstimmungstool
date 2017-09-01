from django.core.management.base import BaseCommand, CommandError
from voty.initproc.models import Quorum
from django.contrib.auth import get_user_model
from math import ceil

"""
- Bis 99 Abstimmungsberechtigten 10 Personen
- ab 100 bis 299 Abstimmungsberechtigten 15 Personen
- ab 300 bis 599 Abstimmungsberechtigten 20 Personen
- ab 600 bis 999 Abstimmungsberechtigten 30 Personen
- ab 1000 bis 1999 Abstimmungsberechtigten 35 Personen
- ab 2000 bis 4999 Abstimmungsberechtigten 50 Personen
- ab 5000 Abstimmungsberechtigten 1% der Abstimmungsberechtigten
"""

class Command(BaseCommand):
    help = "Calculate the next quorum and set it"

    def handle(self, *args, **options):
        total = get_user_model().objects.filter(is_active=True).count()
        quorum = ceil(total / 100.0)

        if total < 100:
            quorum = 10
        elif total < 300:
            quorum = 15
        elif total < 600:
            quorum = 20
        elif total < 1000:
            quorum = 30
        elif total < 2000:
            quorum = 35
        elif total < 5000:
            quorum = 50

        Quorum(quorum=quorum).save()

        print("Total: {} -- Quorum set to {}".format(total, quorum))