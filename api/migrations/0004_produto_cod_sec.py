# Generated by Django 3.1.7 on 2021-07-22 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_produto_cod_ncm'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='cod_sec',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
