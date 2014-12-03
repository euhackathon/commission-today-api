from tastypie.constants import ALL
from tastypie.fields import ToOneField
from tastypie.resources import ModelResource
from backend.models import Portofolio, Member, Meeting, Organization
import calendar
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from tastypie.utils import trailing_slash
from django.http import Http404
from django.conf.urls import url


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
        limit = 1000
        queryset = Member.objects.all()
        allowed_methods = ['get']


class OrganizationResource(ModelResource):
    class Meta:
        limit = 1000
        queryset = Organization.objects.all()
        allowed_methods = ['get']


class MeetingResource(ModelResource):
    member = ToOneField(MemberResource, 'member', full=True)
    organization = ToOneField(OrganizationResource, 'organization', full=True,
                              null=True)
    class Meta:
        limit = 1000
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

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        # Do the query.
        sqs = SearchQuerySet().models(Meeting).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return self.create_response(request, object_list)
