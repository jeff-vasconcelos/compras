# Generated by Django 3.1.7 on 2021-07-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_dadosestoque'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosestoque',
            name='ruptura',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
