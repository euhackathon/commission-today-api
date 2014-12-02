from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from backend.models import Meeting


class Command(BaseCommand):
    help = 'Just some statistics'

    def handle(self, *args, **options):
        for meeting in Meeting.objects.all():
            print "{0};{1}".format(meeting.description.encode('utf-8'), meeting.member.portofolio.name)
