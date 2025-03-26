from django.core.management.base import BaseCommand
from api.models import CacheLog
from django.utils.timezone import now
from datetime import timedelta

class Command(BaseCommand):
    help = "Limpa logs de cache mais antigos (30 dias)."

    def handle(self, *args, **kwargs):
        limite_data = now() - timedelta(days=30)
        deletados, _ = CacheLog.objects.filter(data_hora__lt=limite_data).delete()
        self.stdout.write(self.style.SUCCESS(f"{deletados} registros antigos de cache foram excluídos."))
