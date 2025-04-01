from rest_framework import serializers
from .models import RegraRPG, FonteRPG, RegraRPG, Magia, ClasseRPG

class FonteRPGSerializer(serializers.ModelSerializer):
    sistema_nome = serializers.CharField(source='sistema.nome', read_only=True)

    class Meta:
        model = FonteRPG
        fields = ['id', 'nome', 'tipo', 'ordem', 'sistema', 'sistema_nome']
        read_only_fields = ['id', 'sistema_nome']

class RegraRPGSerializer(serializers.ModelSerializer):
    fonte_nome = serializers.CharField(source='fonte.nome', read_only=True)
    sistema_nome = serializers.CharField(source='fonte.sistema.nome', read_only=True)

    class Meta:
        model = RegraRPG
        fields = ['id', 'titulo', 'categoria', 'descricao', 'tags', 'fonte', 'fonte_nome', 'sistema_nome', 'criado_em']
        read_only_fields = ['id', 'fonte_nome', 'sistema_nome', 'criado_em']

class MagiaSerializer(serializers.ModelSerializer):
    sistema_nome = serializers.CharField(source='sistema.nome', read_only=True)

    class Meta:
        model = Magia
        fields = [
            'id', 'nome', 'nivel', 'escola', 'tempo_conjuracao',
            'alcance', 'componentes', 'duracao', 'ritual',
            'concentracao', 'descricao', 'tags', 'sistema', 'sistema_nome', 'criado_em'
        ]
        read_only_fields = ['id', 'sistema_nome', 'criado_em']

class ClasseRPGSerializer(serializers.ModelSerializer):
    sistema_nome = serializers.CharField(source='sistema.nome', read_only=True)

    class Meta:
        model = ClasseRPG
        fields = [
            'id', 'nome', 'descricao', 'dados_vida', 'proficiencias',
            'pericias_disponiveis', 'habilidades_nivel', 'magias_conhecidas',
            'sistema', 'sistema_nome', 'criado_em'
        ]
        read_only_fields = ['id', 'sistema_nome', 'criado_em']