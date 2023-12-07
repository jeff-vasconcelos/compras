from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from app.models import Pedido


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def delete_orders_by_company(request, pk):
    try:

        qs_orders = Pedido.objects.filter(empresa_id=pk,
                                          num_pedido=request.data['num_pedido'],
                                          cod_produto=request.data['cod_produto']).first()

        if not qs_orders:
            return JsonResponse({"error": "order not found"}, status=404)

        qs_orders.delete()

        return JsonResponse({"success": "orders successfully removed"}, status=200)

    except Exception as e:
        raise e
