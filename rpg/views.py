from rest_framework.views import APIView
from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status, permissions
import fitz  # PyMuPDF
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from api.models import SistemaRPG
from rpg.models import FonteRPG, RegraRPG, Magia, ClasseRPG
from rpg.serializers import FonteRPGSerializer, RegraRPGSerializer, MagiaSerializer, ClasseRPGSerializer

CATEGORIAS = {
    "Combate": ["iniciativa", "ataque", "ação", "movimento", "dano", "acerto", "rolagem"],
    "Perícia": ["teste", "perícia", "furtividade", "persuasão", "intimidação"],
    "Magia": ["magia", "conjuração", "nível de magia", "componentes", "efeito"],
    "Exploração": ["viagem", "dungeon", "ambiente", "armadilha", "navegação"],
    "Interação Social": ["npc", "interação", "diálogo", "convencimento"],
    "Criação de Personagem": ["raça", "classe", "atributo", "antecedente", "origem"],
}

def classificar_categoria(texto):
    texto = texto.lower()
    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in texto:
                return categoria
    return "Indefinida"

def gerar_tags(texto):
    tokens = word_tokenize(texto.lower())
    palavras_validas = [
        palavra for palavra in tokens
        if palavra.isalpha() and palavra not in stopwords.words("portuguese")
    ]
    # Retorna até 5 palavras-chave únicas
    return list(dict.fromkeys(palavras_validas))[:5]

class FonteRPGViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FonteRPG.objects.all().order_by('ordem')
    serializer_class = FonteRPGSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sistema', 'tipo']

class RegraRPGViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegraRPG.objects.all()
    serializer_class = RegraRPGSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['fonte', 'fonte__sistema', 'categoria', 'tags']
    search_fields = ['titulo', 'descricao', 'tags']

class ImportarLivroAPIView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAdminUser]  # ou customize depois

    def post(self, request, format=None):
        arquivo = request.FILES.get("arquivo")
        nome_fonte = request.data.get("nome_fonte")
        tipo_fonte = request.data.get("tipo_fonte")
        sistema_id = request.data.get("sistema_id")

        if not all([arquivo, nome_fonte, tipo_fonte, sistema_id]):
            return Response({"erro": "Campos obrigatórios: arquivo, nome_fonte, tipo_fonte, sistema_id"}, status=400)

        try:
            sistema = SistemaRPG.objects.get(id=sistema_id)
        except SistemaRPG.DoesNotExist:
            return Response({"erro": "SistemaRPG inválido"}, status=404)

        # Cria a FonteRPG
        fonte, _ = FonteRPG.objects.get_or_create(
            sistema=sistema,
            nome=nome_fonte,
            defaults={"tipo": tipo_fonte, "ordem": 0}
        )

        # Lê o conteúdo do PDF
        texto = ""
        if arquivo.name.endswith(".pdf"):
            with fitz.open(stream=arquivo.read(), filetype="pdf") as doc:
                for pagina in doc:
                    texto += pagina.get_text()
        elif arquivo.name.endswith(".txt"):
            texto = arquivo.read().decode("utf-8")
        else:
            return Response({"erro": "Formato de arquivo não suportado. Use PDF ou TXT."}, status=400)

        # Separação heurística dos blocos de regras
        padrao_titulo = re.compile(r"\n([A-Z][A-Z\s\-:]{5,})\n")
        partes = padrao_titulo.split(texto)
        blocos = []
        for i in range(1, len(partes), 2):
            titulo = partes[i].strip()
            corpo = partes[i + 1].strip()
            blocos.append({"titulo": titulo, "descricao": corpo})

        # Criação no banco
        regras_criadas = []
        for bloco in blocos:
            categoria = classificar_categoria(bloco["titulo"] + " " + bloco["descricao"])
            tags = gerar_tags(bloco["titulo"] + " " + bloco["descricao"])

            regra, criada = RegraRPG.objects.get_or_create(
                fonte=fonte,
                titulo=bloco["titulo"],
                defaults={
                    "categoria": categoria,
                    "descricao": bloco["descricao"],
                    "tags": tags
                }
            )
            if criada:
                regras_criadas.append(regra.titulo)

        return Response({
            "mensagem": f"{len(regras_criadas)} regras importadas com sucesso.",
            "fonte_id": fonte.id,
            "sistema": sistema.nome,
            "regras": regras_criadas[:10]  # mostra só os 10 primeiros para preview
        }, status=201)
    
class MagiaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Magia.objects.all()
    serializer_class = MagiaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sistema', 'escola', 'nivel', 'ritual', 'concentracao']
    search_fields = ['nome', 'descricao', 'tags']

class ClasseRPGViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClasseRPG.objects.all()
    serializer_class = ClasseRPGSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['sistema']
    search_fields = ['nome', 'descricao', 'proficiencias', 'pericias_disponiveis']