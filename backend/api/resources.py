from tastypie.resources import ModelResource
from backend.models import Portofolio


class PortofolioResource(ModelResource):
    class Meta:
        queryset = Portofolio.objects.all()
        allowed_methods = ['get']
