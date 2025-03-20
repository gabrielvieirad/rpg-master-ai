from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin
from .models import SistemaRPG, Personagem, Campanha, CustomUser  # Removendo Mestre

@admin.register(SistemaRPG)
class SistemaRPGAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sistema')

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mestre', 'sistema')

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
