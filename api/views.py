from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import link
from rest_framework.response import Response
from .serializers import RegionSerializer, CitySerializer
from district.models import Region, City


class RegionViewSet(ReadOnlyModelViewSet):
    model = Region
    serializer_class = RegionSerializer
    lookup_field = 'id'

    @link()
    def cities(self, request, id):
        region = self.get_object()
        cities = region.cities.all()
        return Response([city.to_json() for city in cities])


class CityViewSet(ReadOnlyModelViewSet):
    model = City
    serializer_class = CitySerializer
