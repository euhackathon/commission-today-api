from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from backend.models import Member, Portofolio
import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://ec.europa.eu/commission/2014-2019/'

class Command(BaseCommand):
    help = 'Scrape data from the website'

    def handle(self, *args, **options):
        self.update_members_urls()
        members = Member.objects.all()
        # for member in members:
        #     self.parse_member(member)

    def update_members_urls(self):
        """Parse http://ec.europa.eu/commission/2014-2019/, get the URLs and
        send them to the database in the members table. Do this every time,
        because maybe the URLs may have changed.
        """
        try:
            request = requests.get(BASE_URL)
        except requests.exceptions.RequestException as e:
            print e
            return

        soup = BeautifulSoup(request.content)
        bigDiv = soup.find(id='quicktabs-tabpage-team_members-0')
        members = bigDiv.find_all(class_='views-row')
        for member in members:
            url = member.find('a')['href']
            photoUrl = member.find('img')['src']
            name = member.find(class_='member-details-name').get_text()
            rank = member.find(class_='role').get_text()
            portofolio = member.find(class_='member-details-text-2').get_text()

            if not Portofolio.objects.filter(name=portofolio):
                portofolioModel = Portofolio(name=portofolio)
                portofolioModel.save()

            if not Member.objects.filter(name=name):
                memberModel = Member(name=name,
                                     photoUrl=photoUrl,
                                     rank=rank,
                                     portofolio=portofolioModel,
                                     url=url)
                memberModel.save()
                print 'saved', name
            else:
                print 'was already saved', name

    def parse_member(self, member):
        """Parse every member in the database and add his agenda to our
        database.
        """
        pass
