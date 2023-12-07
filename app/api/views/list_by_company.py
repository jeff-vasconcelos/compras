from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import Produto, Fornecedor, Pedido
from app.serializers.branch_serializer import BranchesGetSerializer
from app.serializers.order_serializer import OrdersGetSerializer
from app.serializers.product_serializer import ProductsGetSerializer
from app.serializers.provider_serializer import ProvidersGetSerializer
from core.models.empresas_models import Filial


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def list_products_by_company(request, pk):
    qs = Produto.objects.filter(empresa_id=pk,
                                is_active=True).order_by('-id')
    serializer = ProductsGetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def list_providers_by_company(request, pk):
    qs = Fornecedor.objects.filter(empresa_id=pk).order_by('-id')
    serializer = ProvidersGetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def list_branches_by_company(request, pk):
    qs = Filial.objects.filter(empresa_id=pk).order_by('-id')
    serializer = BranchesGetSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def list_orders_by_company(request, pk):
    start_date = datetime.date.today()
    end_date = start_date - datetime.timedelta(days=90)

    qs = Pedido.objects.filter(empresa_id=pk,
                               data__range=[end_date, start_date],
                               produto__is_active=True).order_by('-id')
    serializer = OrdersGetSerializer(qs, many=True)
    return Response(serializer.data)
