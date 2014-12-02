from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from backend.models import Member, Portofolio, Meeting
import requests
from bs4 import BeautifulSoup


BASE_URL = 'http://ec.europa.eu/commission/2014-2019/'

class Command(BaseCommand):
    help = 'Scrape data from the website'

    def handle(self, *args, **options):
        self.update_members_urls()
        members = Member.objects.all()
        for member in members:
            # self.parse_member(member)
            self.parse_cabinet(member)

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

        # Also get the president because he is special
        if not Member.objects.filter(name='Jean-Claude Juncker'):
            president = soup.find(class_='team-members-president')
            url = president.find('a')['href']
            photoUrl = president.find('img')['src']
            name = 'Jean-Claude Juncker'
            rank = 'President'
            portofolioModel = Portofolio(name='President')
            portofolioModel.save()
            presidentModel = Member(name=name,
                                    photoUrl=photoUrl,
                                    rank=rank,
                                    portofolio=portofolioModel,
                                    url=url)
            presidentModel.save()

    def parse_cabinet(self, member):
        try:
            request = requests.get(member.url)
        except requests.exceptions.RequestException as e:
            print e
            return

        soup = BeautifulSoup(request.content)
        urls = soup.find_all(class_='views-field-field-biography-agenda-text')[0].find_all('a')

        # TODO @palcu: parse also the first table when we have an example
        self.parse_table(urls[1]['href'], member)

    def parse_table(self, url, member):
        """I am not proud of what is written down here but, at least it works.
        """
        try:
            request = requests.get(url)
        except requests.exceptions.RequestException as e:
            print e
            return

        soup = BeautifulSoup(request.content)
        rows = soup.find_all('tr')[1:]
        for row in rows:
            cells = row.find_all('td')
            # TODO @palcu: fix me !!!
            try:
                description = 'Meeting with {0} on {1}.'.format(cells[3].get_text().strip(),
                                                                cells[4].get_text().strip())
            except Exception as e:
                continue
            # TODO @palcu: fix me !!!
            try:
                date = datetime.strptime(cells[1].get_text().strip(), '%d/%m/%Y')
            except Exception as e:
                continue
            # TODO @palcu: fix me !!!
            try:
                memberName = cells[0].get_text().strip()
            except Exception as e:
                continue
            if not Member.objects.filter(name=memberName):
                memberModel = Member(name=memberName,
                                     rank='Cabinet',
                                     portofolio=member.portofolio)
                memberModel.save()
                print 'saved'
            else:
                print 'already saved'
            memberModel = Member.objects.get(name=memberName)
            meeting = Meeting(date=date,
                              description=description,
                              member=memberModel,
                              lobby=True)
            meeting.save()

    def parse_member(self, member):
        """Parse every member in the database and add his agenda to our
        database.
        """
        url = member.url.split('_')[0] + '/agenda_en'
        try:
            request = requests.get(url)
        except requests.exceptions.RequestException as e:
            print e
            return

        soup = BeautifulSoup(request.content)
        meetings = soup.find_all(class_='views-row')

        # Skip the first item because it is the header
        meetings = meetings[1:]

        for meeting in meetings:
            description = meeting.find('h3').get_text()
            date = self.get_date_of_meeting(meeting.find(class_='day').get_text())
            if not Meeting.objects.filter(member=member,
                                  description=description,
                                  date=date):
                meeting = Meeting(member=member,
                                  description=description,
                                  date=date,
                                  lobby=False)
                meeting.save()
                print 'saved', description
            else:
                print 'already saved', description

    def get_date_of_meeting(self, dayString):
        try:
            day = int(dayString)
        except ValueError as e:
            print 'Could not convert {0} to int.'.format(dayString)
            # TODO @palcu: fix this
            day = datetime.now().day

        return datetime(month=datetime.now().month,
                        year=datetime.now().year,
                        day=day)
