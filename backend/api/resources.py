from tastypie.constants import ALL
from tastypie.fields import ToOneField
from tastypie.resources import ModelResource
from backend.models import Portofolio, Member, Meeting
import calendar


class PortofolioResource(ModelResource):
    class Meta:
        queryset = Portofolio.objects.all()
        allowed_methods = ['get']

    def dehydrate(self, bundle):
        bundle = super(PortofolioResource, self).dehydrate(bundle)
        shorthand = bundle.data.get('shorthand', '')
        if shorthand != '':
            bundle.data['name'] = shorthand
        bundle.data.pop('shorthand')
        return bundle


class MemberResource(ModelResource):
    portofolio = ToOneField(PortofolioResource, 'portofolio', full=True)
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

    def dehydrate_date(self, bundle):
        """Fucking UNIX timestamps."""
        x = bundle.data['date']
        return calendar.timegm(x.timetuple())
