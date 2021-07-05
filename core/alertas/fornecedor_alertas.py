from api.models.fornecedor import Fornecedor


def get_fornecedores(id_empresa):
    fornecedores = Fornecedor.objects.filter(empresa__id__exact=id_empresa)
    return fornecedores
