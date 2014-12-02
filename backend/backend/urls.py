from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from backend.models import Portofolio, Member, Meeting, Organization
from api.resources import (PortofolioResource, MemberResource, MeetingResource,
                           OrganizationResource)


v1_api = Api(api_name='v1')
v1_api.register(PortofolioResource())
v1_api.register(MemberResource())
v1_api.register(MeetingResource())
v1_api.register(OrganizationResource())

admin.site.register(Portofolio)
admin.site.register(Member)
admin.site.register(Meeting)
admin.site.register(Organization)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls))
)
