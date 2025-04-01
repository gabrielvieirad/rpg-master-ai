from django.db import models
from api.models import SistemaRPG  # Importando o sistema criado no app API

class RegraRPG(models.Model):
    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="regras")
    titulo = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    tags = models.JSONField(default=list, blank=True)  # Lista de palavras-chave
    fonte = models.CharField(max_length=255, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.sistema.nome})"

class FonteRPG(models.Model):
    TIPO_LIVRO = [
        ("jogador", "Livro do Jogador"),
        ("mestre", "Guia do Mestre"),
        ("monstros", "Livro dos Monstros"),
        ("suplemento", "Suplemento"),
    ]

    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="fontes")
    nome = models.CharField(max_length=255)  # Ex: "Livro do Jogador"
    tipo = models.CharField(max_length=50, choices=TIPO_LIVRO)
    ordem = models.PositiveIntegerField(default=0)  # Para organizar visualmente os livros

    def __str__(self):
        return f"{self.nome} ({self.sistema.nome})"

class Magia(models.Model):
    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="magias")
    nome = models.CharField(max_length=255)
    nivel = models.PositiveIntegerField()
    escola = models.CharField(max_length=100)
    tempo_conjuracao = models.CharField(max_length=100)
    alcance = models.CharField(max_length=100)
    componentes = models.CharField(max_length=100)
    duracao = models.CharField(max_length=100)
    descricao = models.TextField()
    ritual = models.BooleanField(default=False)
    concentracao = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} (Nível {self.nivel}) - {self.sistema.nome}"

class ClasseRPG(models.Model):
    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="classes")
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    dados_vida = models.CharField(max_length=50)
    proficiencias = models.TextField(blank=True, null=True)
    pericias_disponiveis = models.TextField(blank=True, null=True)
    habilidades_nivel = models.JSONField(default=dict, blank=True)  # Ex: {"1": ["Fúria", "Defesa"], "2": ["Ataque Extra"]}
    magias_conhecidas = models.JSONField(default=dict, blank=True)  # Se for classe mágica
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.sistema.nome})"

class RacaRPG(models.Model):
    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="racas")
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    modificadores_atributos = models.JSONField(default=dict, blank=True)  # Ex: {"for": +2, "des": +1}
    habilidades = models.TextField(blank=True, null=True)
    idiomas = models.TextField(blank=True, null=True)
    tamanho = models.CharField(max_length=50, blank=True, null=True)
    deslocamento = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.sistema.nome})"
