from core.models.empresas_models import Filial

from api.models.fornecedor import Fornecedor
from api.models.produto import Produto
from api.models.venda import Venda
from api.models.historico import Historico
from api.models.pedido import Pedido
from api.models.entrada import Entrada
from api.models.estoque import Estoque


class ValidExistsData:
    @staticmethod
    def provider_exists(data):
        provider_query = Fornecedor.objects.filter(cod_fornecedor=data['cod_fornecedor'],
                                                   empresa=data['empresa']).first()

        if provider_query:
            return provider_query
        return False

    @staticmethod
    def product_exists(data):
        product_query = Produto.objects.filter(cod_produto=data['cod_produto'],
                                               empresa=data['empresa']).first()

        if product_query:
            return product_query
        return False

    @staticmethod
    def branch_exists(data):
        branch_query = Filial.objects.filter(cod_filial=data['cod_filial'],
                                             empresa=data['empresa']).exists()

        if branch_query:
            return True
        return False

    @staticmethod
    def sale_exists(data):
        sale_query = Venda.objects.filter(cod_produto=data['cod_produto'],
                                          empresa=data['empresa'],
                                          cod_filial=data['cod_filial'],
                                          cod_fornecedor=data['cod_fornecedor'],
                                          data=data['data'],
                                          qt_venda=data['qt_venda'],
                                          preco_unitario=data['preco_unitario'],
                                          custo_financeiro=data['preco_unitario'],
                                          cliente=data['cliente'],
                                          num_nota=data['num_nota']).first()

        if sale_query:
            return True
        return False

    @staticmethod
    def history_exists(data):
        history_query = Historico.objects.filter(cod_produto=data['cod_produto'],
                                                 cod_filial=data['cod_filial'],
                                                 empresa=data['empresa'],
                                                 cod_fornecedor=data['cod_fornecedor'],
                                                 qt_estoque=data['qt_estoque'],
                                                 data=data['data']).first()

        if history_query:
            return True
        return False

    @staticmethod
    def entry_exists(data):
        entry_query = Entrada.objects.filter(cod_produto=data['cod_produto'],
                                             cod_filial=data['cod_filial'],
                                             empresa=data['empresa'],
                                             qt_ult_entrada=data['qt_ult_entrada'],
                                             cod_fornecedor=data['cod_fornecedor'],
                                             data=data['data']).first()

        if entry_query:
            return True
        return False

    @staticmethod
    def order_exists(data):
        order_query = Pedido.objects.filter(cod_produto=data['cod_produto'],
                                            cod_filial=data['cod_filial'],
                                            empresa=data['empresa'],
                                            cod_fornecedor=data['cod_fornecedor'],
                                            num_pedido=data['num_pedido'],
                                            data=data['data']).first()

        if order_query:
            return order_query
        return False

    @staticmethod
    def stock_exists(data):
        stock_query = Estoque.objects.filter(cod_produto=data['cod_produto'],
                                             cod_filial=data['cod_filial'],
                                             empresa=data['empresa'],
                                             cod_fornecedor=data['cod_fornecedor']).first()

        if stock_query:
            return stock_query
        return False


class ProviderCheckUpdate:
    @classmethod
    def check_provider_data(cls, data, provider_query):
        list_data = [data['desc_fornecedor'],
                     data['cnpj'],
                     data['iestadual']]

        list_provider = [provider_query.desc_fornecedor,
                         provider_query.cnpj,
                         provider_query.iestadual]

        len_diff = []

        for a, b in zip(list_data, list_provider):
            if a != b:
                len_diff.append('update')

        if len(len_diff) > 0:
            cls.update_provider(data, provider_query)

    @classmethod
    def update_provider(cls, data, provider_query):
        try:

            provider_query.desc_fornecedor = data['desc_fornecedor']
            provider_query.cnpj = data['cnpj']
            provider_query.iestadual = data['iestadual']

            provider_query.save()

        except Exception as e:
            raise e


class ProductCheckUpdate:
    @classmethod
    def check_product_data(cls, data, product_query):
        list_data = [data['desc_produto'], data['cod_fornecedor'],
                     data['cod_departamento'], data['desc_departamento'],
                     data['cod_secao'], data['desc_secao']]

        list_product = [product_query.desc_produto, product_query.cod_fornecedor,
                        product_query.cod_departamento, product_query.desc_departamento,
                        product_query.cod_secao, product_query.desc_secao]

        len_diff = []

        for a, b in zip(list_data, list_product):
            if a != b:
                len_diff.append('update')

        if len(len_diff) > 0:
            cls.update_product(data, product_query)

    @classmethod
    def update_product(cls, data, product_query):
        try:

            product_query.desc_produto = data['desc_produto']
            product_query.cod_fornecedor = data['cod_fornecedor']
            product_query.cod_departamento = data['cod_departamento']
            product_query.cod_secao = data['cod_secao']
            product_query.desc_departamento = data['desc_departamento']
            product_query.desc_secao = data['desc_secao']

            product_query.save()

        except Exception as e:
            raise e


class StockCheckUpdate:
    @classmethod
    def check_stock_data(cls, data, stock_query):
        list_data = [data['data'], data['qt_geral'],
                     data['qt_bloqueada'], data['qt_indenizada'],
                     data['qt_pendente'], data['qt_disponivel'],
                     data['qt_reservada']]

        list_stock = [stock_query.data, stock_query.qt_geral,
                      stock_query.qt_bloqueada, stock_query.qt_indenizada,
                      stock_query.qt_pendente, stock_query.qt_disponivel,
                      stock_query.qt_reservada]

        len_diff = []

        for a, b in zip(list_data, list_stock):
            if a != b:
                len_diff.append('update')

        if len(len_diff) > 0:
            cls.update_stock(data, stock_query)

    @classmethod
    def update_stock(cls, data, stock_query):
        try:

            stock_query.data = data['data']
            stock_query.qt_geral = data['qt_geral']
            stock_query.qt_bloqueada = data['qt_bloqueada']
            stock_query.qt_indenizada = data['qt_indenizada']
            stock_query.qt_pendente = data['qt_pendente']
            stock_query.qt_disponivel = data['qt_disponivel']
            stock_query.qt_reservada = data['qt_reservada']

            stock_query.save()

        except Exception as e:
            raise e


class OrderCheckUpdate:
    @classmethod
    def check_order_data(cls, data, order_query):

        if data['saldo'] != order_query.saldo:
            cls.update_order(data, order_query)

    @classmethod
    def update_order(cls, data, order_query):
        try:

            order_query.saldo = data['saldo']

            order_query.save()

        except Exception as e:
            raise e
