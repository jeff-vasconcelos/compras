# # import datetime
# # from django.utils import timezone
# # import pytz
# #
# # from django.db.models import Q
# # from django.http import JsonResponse
# # from rest_framework import generics
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view, permission_classes
# # from rest_framework.permissions import IsAuthenticated, AllowAny
# # from app.serializer_integration import *
# # from core.models.empresas_models import Filial
# #
# #
# # @api_view(['GET', ])
# # @permission_classes((IsAuthenticated, ))
# # def access_valid(request):
# #
# #     return Response("API - Insight")
# #
# #
# @api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
# def list_products_by_company(request, pk):
#     qs = Produto.objects.filter(empresa_id=pk,
#                                 is_active=True).order_by('-id')
#     serializer = ProductsGetSerializer(qs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
# def list_providers_by_company(request, pk):
#     qs = Fornecedor.objects.filter(empresa_id=pk).order_by('-id')
#     serializer = ProvidersGetSerializer(qs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
# def list_branches_by_company(request, pk):
#     qs = Filial.objects.filter(empresa_id=pk).order_by('-id')
#     serializer = BranchesGetSerializer(qs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET', ])
# @permission_classes((IsAuthenticated, ))
# def list_orders_by_company(request, pk):
#
#     start_date = datetime.date.today()
#     end_date = start_date - datetime.timedelta(days=90)
#
#     qs = Pedido.objects.filter(empresa_id=pk,
#                                data__range=[end_date, start_date],
#                                produto__is_active=True).order_by('-id')
#     serializer = OrdersGetSerializer(qs, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['POST', ])
# @permission_classes((IsAuthenticated, ))
# def delete_orders_by_company(request, pk):
#     try:
#
#         qs_orders = Pedido.objects.filter(empresa_id=pk,
#                                           num_pedido=request.data['num_pedido'],
#                                           cod_produto=request.data['cod_produto']).first()
#
#         if not qs_orders:
#             return JsonResponse({"error": "order not found"}, status=404)
#
#         qs_orders.delete()
#
#         return JsonResponse({"success": "orders successfully removed"}, status=200)
#
#     except Exception as e:
#         raise e
#
#
# @api_view(['POST', ])
# @permission_classes((IsAuthenticated, ))
# def inactive_product_by_company(request, pk):
#     try:
#
#         product_query = Produto.objects.filter(cod_produto=request.data['cod_produto'],
#                                                empresa_id=pk).first()
#
#         if not product_query:
#             return JsonResponse({"message": "product not found"}, status=404)
#
#         product_query.is_active = False
#         product_query.save()
#
#         return JsonResponse({"message": "the product is no longer active"}, status=200)
#
#     except Exception as e:
#         raise e
