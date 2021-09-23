from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.serializer_integration import *


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def fornecedor_create(request, *args, **kwargs):
    serializer = FornecSerializer(data=request.data, many=isinstance(request.data, list))
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def produto_create(request, *args, **kwargs):
    serializer = ProdSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def historico_create(request, *args, **kwargs):
    serializer = HistSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def venda_create(request, *args, **kwargs):
    serializer = VendaSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def pedido_create(request, *args, **kwargs):
    serializer = PedSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def entrada_create(request, *args, **kwargs):
    serializer = EntSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def estoque_create(request, *args, **kwargs):
    serializer = EstSerializer(data=request.data, many=isinstance(request.data, list))

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
