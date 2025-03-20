import django_filters
from .models import Personagem, SistemaRPG

class PersonagemFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')
    sistema = django_filters.NumberFilter(field_name="sistema__id")

    class Meta:
        model = Personagem
        fields = ['nome', 'sistema']

class SistemaRPGFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SistemaRPG
        fields = ['nome']
