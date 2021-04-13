# Generated by Django 3.1.7 on 2021-04-13 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_empresa_cep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='cnpj',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='estado',
            field=models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espirito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='numero',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
