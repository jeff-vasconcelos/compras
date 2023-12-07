from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from app.models import Produto


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def inactive_product_by_company(request, pk):
    try:

        product_query = Produto.objects.filter(cod_produto=request.data['cod_produto'],
                                               empresa_id=pk).first()

        if not product_query:
            return JsonResponse({"message": "product not found"}, status=404)

        product_query.is_active = False
        product_query.save()

        return JsonResponse({"message": "the product is no longer active"}, status=200)

    except Exception as e:
        raise e
