from api.models.produto import Produto


def get_produtos(id_empresa, id_fornecedor):
    produtos = Produto.objects.filter(empresa__id__exact=id_empresa, fornecedor__id=id_fornecedor)
    return produtos
