from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import PersonagemViewSet, SistemaRPGViewSet, CampanhaViewSet, CustomTokenObtainPairView, GerarHistoriaAPIView, HistoriaGeradaViewSet, LogAtividadeViewSet, CacheLogViewSet


router = DefaultRouter()
router.register(r'personagens', PersonagemViewSet, basename="personagem")
router.register(r'sistemas', SistemaRPGViewSet, basename="sistema")
router.register(r'campanhas', CampanhaViewSet)
router.register(r'historias', HistoriaGeradaViewSet, basename="historias")
router.register(r'logs', LogAtividadeViewSet, basename='logs')
router.register(r'logs-atividade', LogAtividadeViewSet, basename='logs-atividade')
router.register(r'cache-logs', CacheLogViewSet, basename="cache-logs")



urlpatterns = [
    path('', include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('campanhas/solo/', CampanhaViewSet.as_view({'post': 'criar_solo'}), name='campanha-solo'),
    path('gerar-historia/', GerarHistoriaAPIView.as_view(), name="gerar_historia"),

]