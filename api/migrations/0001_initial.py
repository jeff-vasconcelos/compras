# Generated by Django 3.1.7 on 2021-11-12 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_fornecedor', models.IntegerField()),
                ('desc_fornecedor', models.CharField(max_length=255)),
                ('cnpj', models.CharField(blank=True, max_length=255, null=True)),
                ('iestadual', models.CharField(blank=True, max_length=255, null=True)),
                ('leadtime', models.IntegerField(blank=True, null=True)),
                ('ciclo_reposicao', models.IntegerField(blank=True, null=True)),
                ('tempo_estoque', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fonecedor_empresa', to='core.empresa')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedor',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('desc_produto', models.CharField(max_length=255)),
                ('embalagem', models.CharField(blank=True, max_length=255, null=True)),
                ('quantidade_un_cx', models.FloatField()),
                ('marca', models.CharField(blank=True, max_length=255, null=True)),
                ('peso_liquido', models.CharField(blank=True, max_length=255, null=True)),
                ('principio_ativo', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_fabrica', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_ncm', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_auxiliar', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_depto', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_sec', models.CharField(blank=True, max_length=255, null=True)),
                ('desc_departamento', models.CharField(blank=True, max_length=255, null=True)),
                ('desc_secao', models.CharField(blank=True, max_length=255, null=True)),
                ('cod_fornecedor', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto', to='core.empresa')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_produto', to='api.fornecedor')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('qt_venda', models.FloatField()),
                ('preco_unit', models.FloatField()),
                ('custo_fin', models.FloatField()),
                ('data', models.DateField()),
                ('cliente', models.CharField(blank=True, max_length=255, null=True)),
                ('num_nota', models.IntegerField(blank=True, null=True)),
                ('rca', models.CharField(blank=True, max_length=255, null=True)),
                ('supervisor', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_venda', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_venda', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_venda', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_venda', to='api.produto')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDuplicado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('saldo', models.FloatField()),
                ('num_pedido', models.IntegerField()),
                ('data', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_pedidosapi', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_pedidosapi', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_pedidosapi', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_pedidosapi', to='api.produto')),
            ],
            options={
                'verbose_name': 'Pedido Existente',
                'verbose_name_plural': 'Pedidos Existentes',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('saldo', models.FloatField()),
                ('num_pedido', models.IntegerField()),
                ('data', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_pedidos', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_pedidos', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_pedidos', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_pedidos', to='api.produto')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('qt_estoque', models.FloatField()),
                ('data', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_historicoestoque', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_historicoestoque', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_historicoestoque', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_historicoestoque', to='api.produto')),
            ],
            options={
                'verbose_name': 'Histórico',
                'verbose_name_plural': 'Históricos',
            },
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('qt_geral', models.FloatField()),
                ('qt_indenizada', models.FloatField()),
                ('qt_reservada', models.FloatField()),
                ('qt_pendente', models.FloatField()),
                ('qt_bloqueada', models.FloatField()),
                ('qt_disponivel', models.FloatField()),
                ('preco_venda', models.FloatField()),
                ('custo_ult_entrada', models.FloatField()),
                ('data', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_estoqueatual', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_estoqueatual', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_estoqueatual', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_estoqueatual', to='api.produto')),
            ],
            options={
                'verbose_name': 'Estoque',
                'verbose_name_plural': 'Estoque',
            },
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_produto', models.IntegerField()),
                ('cod_filial', models.IntegerField()),
                ('cod_fornecedor', models.IntegerField()),
                ('qt_ult_entrada', models.FloatField()),
                ('vl_ult_entrada', models.FloatField()),
                ('data', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('campo_um', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_dois', models.CharField(blank=True, max_length=255, null=True)),
                ('campo_tres', models.CharField(blank=True, max_length=255, null=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresa_entrada', to='core.empresa')),
                ('filial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filial_entrada', to='core.filial')),
                ('fornecedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_entrada', to='api.fornecedor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_entrada', to='api.produto')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
    ]
