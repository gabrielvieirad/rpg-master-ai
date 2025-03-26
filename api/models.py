from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

# Customização do Usuário 
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('mestre', 'Mestre'),
        ('jogador', 'Jogador'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='jogador')

    def is_mestre(self):
        return self.role == 'mestre'
    
    def is_jogador(self):
        return self.role == 'jogador'

# Modelo de Sistemas de RPG 
class SistemaRPG(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

# Modelo de Personagem
class Personagem(models.Model):
    nome = models.CharField(max_length=255)
    sistema = models.ForeignKey("SistemaRPG", on_delete=models.CASCADE, related_name="personagens")
    historia = models.TextField(blank=True, null=True)
    jogador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="personagens", null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.sistema.nome})"

# Modelo de Campanha
class Campanha(models.Model):
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    sistema = models.ForeignKey(SistemaRPG, on_delete=models.CASCADE, related_name="campanhas")
    mestre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="campanhas", null=True, blank=True)

    def __str__(self):
        return self.titulo

# Modelo de Cache de Respostas da IA 
class CacheRespostaIA(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    campanha = models.ForeignKey("Campanha", on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    resposta = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("usuario", "campanha", "prompt")  # Evita duplicação de respostas para o mesmo usuário

    def __str__(self):
        return f"Cache - {self.usuario.username} - {self.campanha} - {self.criado_em}"

# Modelo de Histórico de Interação da IA
class HistoricoIA(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    campanha = models.ForeignKey("Campanha", on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.TextField()
    resposta = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Histórico - {self.usuario.username} - {self.criado_em}"

class HistoriaGerada(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Usuário que gerou a história
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, null=True, blank=True)  # Campanha associada (se houver)
    prompt = models.TextField()  # O prompt que foi enviado para a IA
    resposta = models.TextField()  # A história gerada pela IA
    criado_em = models.DateTimeField(auto_now_add=True)  # Data de criação

    def __str__(self):
        return f'História de {self.usuario.username} - {self.criado_em}'
   
class UsoIA(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantidade_requisicoes = models.IntegerField(default=0) # Contador de requisições
    ultimo_reset = models.DateTimeField(default=now) # Última vez que o contador foi resetado

    def __str__(self):
        return f"{self.usuario.username} - {self.quantidade_requisicoes} requisições"
    
    def resetar_contador(self):
        # Reseta o contador de requisições
        self.quantidade_requisicoes = 0
        self.ultimo_reset = now()
        self.save()

class LogAPI(models.Model):
    # Modelo para armazenar logs de atividades importantes dentro da API
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=255)  # Exemplo: "Criou uma campanha"
    detalhes = models.TextField(blank=True, null=True)  # Pode armazenar informações extras
    data_hora = models.DateTimeField(default=now)  # Quando a ação foi realizada

    def __str__(self):
        return f"{self.data_hora} - {self.usuario} - {self.acao}"
    
class LogAtividade(models.Model):
    """
    Registra atividades importantes realizadas pelos usuários no sistema.
    """
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    acao = models.CharField(max_length=255)  # Exemplo: "Criou uma campanha"
    detalhes = models.TextField(blank=True, null=True)  # Informações adicionais
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data_hora} - {self.usuario} - {self.acao}"

class CacheLog(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cache_usado = models.ForeignKey(CacheRespostaIA, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cache usado por {self.usuario.username} em {self.data_hora}"