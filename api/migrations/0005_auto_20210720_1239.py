# Generated by Django 3.1.7 on 2021-07-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_entrada_custo_ult_entrada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entrada',
            name='custo_ult_entrada',
        ),
        migrations.AddField(
            model_name='estoque',
            name='custo_ult_entrada',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
