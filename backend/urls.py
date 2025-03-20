from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Rota do admin
    path('', include('core.urls')),   # Rota do app "core"
    path('api/', include('api.urls')),  # Rota do app "api"
]