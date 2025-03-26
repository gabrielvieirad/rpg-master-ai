from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter

import openai

from .models import Personagem, SistemaRPG, Campanha, CustomUser, LogAPI, HistoriaGerada, LogAtividade, CacheLog
from .serializers import PersonagemSerializer, SistemaRPGSerializer, CampanhaSerializer
from .filters import PersonagemFilter, SistemaRPGFilter
from .serializers import CampanhaSerializer, HistoriaGeradaSerializer, LogAPISerializer, LogAtividadeSerializer, CacheLogSerializer
from .services import gerar_historia_ia, registrar_log
from .permissions import IsMestre, IsMestreDonoDaCampanha, IsMestreOrReadOnly, IsOwnerOrReadOnly
from .pagination import CustomPagination

from api.permissions import IsMestreDonoDaCampanha
from api.utils import registrar_log, registrar_atividade

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["access"] = str(self.get_token(self.user).access_token) 
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Se "access" não estiver presente, gere manualmente
        if "access" not in response.data:
            user = self.get_user(request.data)
            refresh = RefreshToken.for_user(user)
            response.data["access"] = str(refresh.access_token)

        return response

class CustomPagination(PageNumberPagination):
    page_size = 10 # Defina 10 itens por página
    page_size_query_param = 'page_size'
    max_page_size = 50 # Defina um limite máximo para evitar requisições gigantescas

class PersonagemViewSet(viewsets.ModelViewSet):
    queryset = Personagem.objects.all()
    serializer_class = PersonagemSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PersonagemFilter
    pagination_class = CustomPagination 

class SistemaRPGViewSet(viewsets.ReadOnlyModelViewSet):  
    queryset = SistemaRPG.objects.all()
    serializer_class = SistemaRPGSerializer

# Permissão personalizada: Apenas mestres podem criar campanhas
class IsMestre(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "mestre"

class CampanhaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para criar, listar, editar e excluir campanhas.
    Apenas mestres podem editar suas próprias campanhas.
    """
    queryset = Campanha.objects.all()
    serializer_class = CampanhaSerializer
    permission_classes = [IsMestreDonoDaCampanha]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Filtra campanhas para que jogadores só possam listar.
        """
        if self.request.user.is_authenticated and self.request.user.is_jogador():
            return Campanha.objects.filter(jogadores__jogador=self.request.user)
        return Campanha.objects.all()

    def perform_create(self, serializer):
        serializer.save(mestre=self.request.user)  # A campanha pertence ao mestre

    def perform_update(self, serializer):
        campanha = serializer.save()
        registrar_log(self.request.user, "Edição de campanha", f"Campanha '{campanha.titulo}' foi editada.")

    def perform_destroy(self, instance):
        registrar_log(self.request.user, "Exclusão de campanha", f"Campanha '{instance.titulo}' foi excluída.")
        instance.delete()
        
    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsMestreDonoDaCampanha()]
        return [permissions.IsAuthenticated()]

class GerarHistoriaAPIView(APIView):
    permission_classes = [IsMestre]

    def post(self, request):
        if not request.user.is_mestre():
            return Response({"error": "Apenas mestres podem gerar histórias."}, status=status.HTTP_403_FORBIDDEN)

        campanha_id = request.data.get("campanha_id")
        tom = request.data.get("tom", "épico")
        genero = request.data.get("genero", "fantasia medieval")
        sistema_rpg = request.data.get("sistema_rpg", "D&D")

        historia = gerar_historia_ia(request.user, campanha_id, tom, genero, sistema_rpg)
        return Response({"historia": historia})
    
class HistoriaGeradaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para listar histórias geradas.
    Apenas o usuário dono da história pode vê-la.
    """
    queryset = HistoriaGerada.objects.all()
    serializer_class = HistoriaGeradaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Filtra histórias para exibir apenas as do usuário autenticado.
        """
        return HistoriaGerada.objects.filter(usuario=self.request.user)

class LogAtividadeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para visualizar os logs de atividade dos usuários.
    Somente administradores têm acesso.
    """
    queryset = LogAtividade.objects.all().order_by("-data_hora")
    serializer_class = LogAtividadeSerializer
    permission_classes = [permissions.IsAdminUser]  # Apenas admins podem visualizar
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["usuario", "acao"]

class CacheLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API para visualizar o uso do cache de respostas da IA.
    Apenas leitura.
    """
    queryset = CacheLog.objects.all().order_by("-data_hora")
    serializer_class = CacheLogSerializer
    permission_classes = [IsAuthenticated]  # Apenas usuários logados podem visualizar