from rest_framework import serializers
from .models import Personagem, SistemaRPG, Campanha, HistoriaGerada, LogAPI, LogAtividade, CacheLog

class PersonagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personagem
        fields = '__all__'  # ou liste os campos explicitamente

class SistemaRPGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaRPG
        fields = '__all__'

class CampanhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campanha
        fields = ["id", "titulo", "descricao", "sistema", "mestre"]

class HistoriaGeradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriaGerada
        fielda = '__all__'

class LogAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAPI
        fields = "__all__"

class LogAtividadeSerializer(serializers.ModelSerializer):
    """
    Serializa os logs de atividade para exibição na API.
    """
    class Meta:
        model = LogAtividade
        fields = "__all__"

class CacheLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CacheLog
        fields = ["id", "usuario", "cache_usado", "data_hora"]