from django.db import models


""" Modelo de empresas """
class Empresa(models.Model):

    ESTADOS = (
        ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"), ("BA", "Bahia"),
        ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espirito Santo"), ("GO", "Goiás"),
        ("MA", "Maranhão"), ("MS", "Mato Grosso do Sul"), ("MT", "Mato Grosso"), ("MG", "Minas Gerais"),
        ("PA", "Pará"), ("PB", "Paraíba"), ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"), ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"),
        ("SC", "Santa Catarina"), ("SP", "São Paulo"), ("SE", "Sergipe"), ("TO", "Tocantins"),
    )

    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    resp_tec = models.CharField(max_length=255, null=True, blank=True,
                                       verbose_name='Responsável técnico')
    resp_leg = models.CharField(max_length=255, null=True, blank=True,
                                       verbose_name='Responsável legal')
    telefone = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    ativo = models.BooleanField(default=False)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=6, null=True, blank=True)
    cidade = models.CharField(max_length=90, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True, choices=ESTADOS)
    cep = models.CharField(max_length=9, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.nome_fantasia
