from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsMestre(permissions.BasePermission):
    """
    Permissão que garante que apenas mestres possam acessar certos recursos.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_mestre()

class IsMestreOrReadOnly(permissions.BasePermission):
    # Permite apenas que mestres editem campanhas, mas qualquer usuário pode visualizar.

    def has_permission(self, request, view):
        # Permitir leitura para qualquer um
        if request.method in permissions.SAFE_METHODS:
            return True
        # Apenas usuários autentificados podem modificar
        return request.user and request.user.is_authenticated and request.user.is_mestre()
    
    def has_object_permission(self, request, view, obj):
        # Permitir leitura para qualquer um
        if request.method in permissions.SAFE_METHODS:
            return True
        # Apenas o mestre dono da campanha pode editar ou deletar
        return obj.mestre == request.user

class IsMestreDonoDaCampanha(permissions.BasePermission):
    """
    Permite apenas que mestres editem suas próprias campanhas.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.mestre == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    # Garante que usuários só possam acessar suas próprias histórias geradas. 

    def has_permission(self, request, view):
        # Permitir leitura para qualquer um autenticado
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permitir leitura para qualquer um autenticado
        if request.method in permissions.SAFE_METHODS:
            return True
        # Apenas o próprio usuário pode acessar suas histórias
        return obj.usuario == request.user