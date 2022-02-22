from rest_framework import viewsets
from .serializer import InformationSerializer
from ..models import Information
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class InformationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Information.objects.all()
    serializer_class = InformationSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['name', 'roll']

    filter_backends = [SearchFilter]
    search_fields = ['name', 'idCard']

    def get_queryset(self):
        return Information.objects.filter(roll__gte=102)
