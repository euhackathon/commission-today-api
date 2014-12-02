import factory
from models import Portofolio, Member, Meeting

class PortofolioFactory(factory.Factory):
  class Meta:
    model = Portofolio

class MemberFactory(factory.Factory):
  class Meta:
    model = Member

class MeetingFactory(factory.Factory):
  class Meta:
    model = Meeting
