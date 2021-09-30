from core.models.empresas_models import Filial


def get_filiais(id_empresa):
    empresa = id_empresa
    filiais = Filial.objects.filter(empresa__id__exact=empresa)
    return filiais

