# Generated by Django 3.2 on 2021-09-28 12:27

import core.models.usuarios_models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_video', models.CharField(blank=True, max_length=255, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Academy',
                'verbose_name_plural': 'Academy',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_fantasia', models.CharField(blank=True, max_length=255, null=True)),
                ('razao_social', models.CharField(blank=True, max_length=255, null=True)),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True)),
                ('iestadual', models.CharField(blank=True, max_length=13, null=True)),
                ('resp_tec', models.CharField(blank=True, max_length=255, null=True, verbose_name='Responsável técnico')),
                ('resp_leg', models.CharField(blank=True, max_length=255, null=True, verbose_name='Responsável legal')),
                ('telefone', models.CharField(blank=True, max_length=14, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('ativo', models.BooleanField(default=False)),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('numero', models.CharField(blank=True, max_length=6, null=True)),
                ('cidade', models.CharField(blank=True, max_length=90, null=True)),
                ('bairro', models.CharField(blank=True, max_length=90, null=True)),
                ('estado', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espirito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MS', 'Mato Grosso do Sul'), ('MT', 'Mato Grosso'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=50, null=True)),
                ('cep', models.CharField(blank=True, max_length=9, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('atualizacao_alerta', models.DateTimeField(blank=True, null=True)),
                ('quantidade_alerta', models.IntegerField(blank=True, null=True)),
                ('envia_email', models.BooleanField(default=True, verbose_name='Enviar E-mails de alerta')),
                ('principio_ativo', models.BooleanField(default=False, verbose_name='Considerar Princípio Ativo')),
                ('qt_usuarios_logados', models.IntegerField(blank=True, null=True, verbose_name='Quantidade de usuários logados')),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoInsight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=255, null=True)),
                ('usuario', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Criado em:')),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_insight', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Pedido Insight',
                'verbose_name_plural': 'Pedidos Insight',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Administrador', 'Administrador'), ('Comprador', 'Comprador')], max_length=15, verbose_name='Tipo')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to=core.models.usuarios_models.get_file_path)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='core.empresa')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoInsightItens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField(blank=True, null=True)),
                ('desc_produto', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_filial', models.IntegerField(blank=True, null=True)),
                ('preco', models.CharField(blank=True, max_length=255, null=True)),
                ('quantidade', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos_insight_itens', to='core.pedidoinsight')),
            ],
            options={
                'verbose_name': 'Item - Pedido Insight',
                'verbose_name_plural': 'Itens - Pedido Insight',
            },
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.IntegerField(blank=True, null=True)),
                ('curva_a', models.FloatField(blank=True, null=True)),
                ('curva_b', models.FloatField(blank=True, null=True)),
                ('curva_c', models.FloatField(blank=True, null=True)),
                ('curva_d', models.FloatField(blank=True, null=True)),
                ('curva_e', models.FloatField(blank=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parametros', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Configuração Empresa',
                'verbose_name_plural': 'Configurações Empresas',
            },
        ),
        migrations.CreateModel(
            name='GraficoFaturamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curva', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grafruptura_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Home - Grafico Dois',
                'verbose_name_plural': 'Home - Grafico Dois',
            },
        ),
        migrations.CreateModel(
            name='GraficoCurva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curva', models.CharField(blank=True, max_length=255, null=True)),
                ('normal', models.CharField(blank=True, max_length=255, null=True)),
                ('parcial', models.CharField(blank=True, max_length=255, null=True)),
                ('excesso', models.CharField(blank=True, max_length=255, null=True)),
                ('total', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grafcurva_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Home - Grafico Um',
                'verbose_name_plural': 'Home - Grafico Um',
            },
        ),
        migrations.CreateModel(
            name='Filial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_filial', models.IntegerField(blank=True, null=True)),
                ('desc_filial', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Filial',
                'verbose_name_plural': 'Filiais',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_empresa', to='core.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='DadosEstoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curva', models.CharField(blank=True, max_length=255, null=True)),
                ('skus', models.IntegerField(blank=True, null=True)),
                ('normal', models.IntegerField(blank=True, null=True)),
                ('parcial', models.IntegerField(blank=True, null=True)),
                ('ruptura', models.IntegerField(blank=True, null=True)),
                ('excesso', models.IntegerField(blank=True, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dadosestoque_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Home - Dados Estoque',
                'verbose_name_plural': 'Home - Dados Estoque',
            },
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_filial', models.IntegerField(blank=True, null=True)),
                ('cod_produto', models.IntegerField(blank=True, null=True)),
                ('desc_produto', models.CharField(blank=True, max_length=255, null=True)),
                ('saldo', models.FloatField(blank=True, null=True)),
                ('sugestao', models.FloatField(blank=True, null=True)),
                ('valor', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_estoque', models.CharField(blank=True, max_length=255, null=True)),
                ('estoque', models.FloatField(blank=True, null=True)),
                ('qt_excesso', models.FloatField(blank=True, null=True)),
                ('vl_excesso', models.CharField(blank=True, max_length=255, null=True)),
                ('curva', models.CharField(blank=True, max_length=255, null=True)),
                ('fornecedor', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_fornecedor', models.IntegerField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_quatro', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alerta_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Alerta',
                'verbose_name_plural': 'Alertas',
            },
        ),
    ]
