from django.urls import path
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Rota funcionando!"})

urlpatterns = [
    path('', home, name='home'),  # Rota principal do app "core"
]