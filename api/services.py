from openai import OpenAI
from django.conf import settings
from .models import HistoriaGerada, Campanha, UsoIA, LogAPI, CacheRespostaIA, HistoricoIA, CacheLog
from django.utils.timezone import now
import difflib

# Limite de requisições por usuario
LIMITE_REQUISICOES = 10 # Define o número máximo de requisições por dia

def encontrar_historia_semelhante(usuario, prompt, campanha_id=None, similaridade_minima=0.85):
    """
    Verifica se já existe uma história semelhante no banco de dados para evitar chamadas desnecessárias à OpenAI.
    """
    historias = HistoriaGerada.objects.filter(usuario=usuario, campanha_id=campanha_id)
    
    for historia in historias:
        similaridade = SequenceMatcher(None, prompt, historia.prompt).ratio()
        if similaridade >= similaridade_minima:
            return historia.resposta  # Retorna a história já existente se for semelhante o suficiente

    return None  # Nenhuma história semelhante encontrada

def verificar_limite_requisicoes(usuario):
    """Verifica se o usurio atingiu o limite diário de requisições"""
    uso, criado = UsoIA.objects.get_or_create(usuario=usuario)

    # Se o último reset foi há mais de 24hrs, resetar o reset
    if (now() - uso.ultimo_reset).days >= 1:
        uso.resetar_contador()
    
    if uso.quantidade_requisicoes >= LIMITE_REQUISICOES:
        return False # Usuário atingiu o limite
    return True

def incrementar_contador_requisicoes(usuario):
    # Adiciona o contador de requisições
    uso, _ = UsoIA.objects.get_or_create(usuario=usuario)
    uso.quantidade_requisicoes += 1
    uso.save()

def gerar_historia_ia(usuario, campanha_id=None, tom="épico", genero="fantasia medieval", sistema_rpg="D&D"):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    prompt = f"Crie um enredo para uma campanha solo de RPG. Gênero: {genero}. Tom: {tom}. Sistema de RPG: {sistema_rpg}."

    # Verifica se já existe uma história semelhante no cache
    historias_existentes = CacheRespostaIA.objects.filter(usuario=usuario)
    for historia in historias_existentes:
        similaridade = difflib.SequenceMatcher(None, historia.prompt, prompt).ratio()
        if similaridade > 0.85:  # Se for mais de 85% semelhante, retorna do cache
            CacheLog.objects.create(usuario=usuario, cache_usado=historia)  # Registra o uso do cache
            return historia.resposta

    # Se não encontrou, gerar nova história com a IA
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um narrador mestre de RPG altamente criativo."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    historia_gerada = response.choices[0].message.content.strip()

    # Salvar no cache e histórico
    cache_resposta = CacheRespostaIA.objects.create(usuario=usuario, campanha_id=campanha_id, prompt=prompt, resposta=historia_gerada)

    if campanha_id:
        campanha = Campanha.objects.get(id=campanha_id)
    else:
        campanha = None

    HistoricoIA.objects.create(usuario=usuario, campanha=campanha, prompt=prompt, resposta=historia_gerada)

    return historia_gerada

def registrar_log(usuario, acao, detalhes=""):
    # Salva um log de uma ação realizada na API.

    LogAPI.objects.create(
        usuario=usuario,
        acao=acao,
        detalhes=detalhes
    )