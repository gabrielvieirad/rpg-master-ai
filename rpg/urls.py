from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegraRPGViewSet, FonteRPGViewSet, ImportarLivroAPIView, MagiaViewSet, ClasseRPGViewSet

router = DefaultRouter()
router.register(r'regras', RegraRPGViewSet, basename='regrarpg')
router.register(r'fontes', FonteRPGViewSet, basename='fonterpg')
router.register(r'magias', MagiaViewSet, basename='magia')
router.register(r'classes', ClasseRPGViewSet, basename='classe')



urlpatterns = [
    path('', include(router.urls)),
    path("importar-livro/", ImportarLivroAPIView.as_view(), name="importar-livro"),

]
