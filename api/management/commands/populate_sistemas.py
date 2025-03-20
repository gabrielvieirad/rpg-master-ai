from django.core.management.base import BaseCommand
from api.models import SistemaRPG

SISTEMAS_INICIAS = [
    {"nome": "Dungeons & Dragons 5e", "descricao": "Um sistema de RPG de fantasia medieval."},
    {"nome": "Call of Cthulhu", "descricao": "RPG de terror investigativo baseado na obra de H.P. Lovecraft."},
    {"nome": "Vampiro: A Máscara", "descricao": "RPG de horror pessoal, onde você interpreta um vampiro."},
    {"nome": "Cyberpunk RED", "descricao": "Um RPG ambientado em um futuro cyberpunk distópico."},
    {"nome": "GURPS", "descricao": "Um sistema genérico e universal para qualquer tipo de cenário."},
]

class Command(BaseCommand):
    help = "Popula o banco de dados com sistemas RPG."

    def handle(self, *args, **kwargs):
        for sistema in SISTEMAS_INICIAS:
            obj, created = SistemaRPG.objects.get_or_create(nome=sistema["nome"], defaults={"descricao": sistema["descricao"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Sistema criado: {sistema["nome"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Sistema já existe: {sistema["nome"]}'))
                