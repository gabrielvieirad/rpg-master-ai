from api.models import LogAPI, LogAtividade

def registrar_log(usuario, acao, detalhes=""):
    LogAPI.objects.create(
        usuario=usuario,
        acao=acao,
        detalhes=detalhes
    )
    
def registrar_atividade(usuario, acao, detalhes=None):
    """
    Registra atividades realizadas pelos usuários no sistema.
    """
    LogAtividade.objects.create(usuario=usuario, acao=acao, detalhes=detalhes)