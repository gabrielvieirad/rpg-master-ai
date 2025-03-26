from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Paginação personalizada para limitação do número de registros que vão ser retornados.
    """
    page_size = 10  # Número de itens por página (pode ser ajustado)
    page_size_query_param = "page_size"
    max_page_size = 100  # Limite máximo para poder evitar sobrecarga
    def get_paginated_response(self, data):
        """
        Retorna a resposta paginada com metadados.
        """
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
