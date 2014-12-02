from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from backend.factories import PortofolioFactory, MemberFactory, MeetingFactory


class Command(BaseCommand):
    help = 'Creates dummy data'

    def handle(self, *args, **options):
        portofolio = PortofolioFactory(name='Digital Single Market')
        portofolio.save()
        member = MemberFactory(portofolio=portofolio,
                               name='Andrus Ansip',
                               rank='Vice-President',
                               url='http://ec.europa.eu/commission/2014-2019/ansip_en',
                               photoUrl='http://ec.europa.eu/commission/sites/cwt/files/styles/biography_portrait_160x160/public/commissioner_portraits/andrus_ansip_2.jpg?itok=o8CtYpOX')
        member.save()
        meeting = MeetingFactory(date=datetime.now(),
                                 description='Visits EU hackathon event',
                                 member=member)
        meeting.save()
