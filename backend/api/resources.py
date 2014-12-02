from tastypie.resources import ModelResource
from backend.models import Portofolio


class PortofolioResource(ModelResource):
    class Meta:
        queryset = Portofolio.objects.all()
        allowed_methods = ['get']

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MeetingResource(ModelResource):
    class Meta:
        queryset = Meeting.objects.all()
        allowed_methods = ['get']
