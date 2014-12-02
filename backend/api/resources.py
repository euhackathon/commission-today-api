from tastypie.constants import ALL
from tastypie.fields import ToOneField
from tastypie.resources import ModelResource
from backend.models import Portofolio, Member, Meeting


class PortofolioResource(ModelResource):
    class Meta:
        queryset = Portofolio.objects.all()
        allowed_methods = ['get']

class MemberResource(ModelResource):
    class Meta:
        queryset = Member.objects.all()
        allowed_methods = ['get']

class MeetingResource(ModelResource):
    member = ToOneField(MemberResource, 'member', full=True)
    class Meta:
        queryset = Meeting.objects.all()
        allowed_methods = ['get']
        filtering = {
            'date': ALL,
            'member': ALL
        }
