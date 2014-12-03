import json
import requests
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from backend.models import Organization


BASE_URL = 'http://api.lobbyfacts.eu/api/1/representative/'

class Command(BaseCommand):
    help = 'Just some statistics'

    def handle(self, *args, **options):
        for organization in Organization.objects.all():
            lobbyfactId = organization.explore_url.split('/')[-1]
            url = BASE_URL + lobbyfactId
            try:
                request = requests.get(url)
            except requests.exceptions.RequestException as e:
                print e
                continue

            data = json.loads(request.content)
            organization.name = data['entity']['name']
            organization.money = max(data['financial_data'][0].get('cost_absolute', 0),
                                     data['financial_data'][0].get('cost_max', 0))
            organization.lobbyists = data.get('members', 0)
            organization.explore_url = url
            organization.save()

            print 'done with', organization.name

