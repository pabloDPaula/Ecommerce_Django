# Generated by Django 4.1 on 2022-12-14 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0009_produto_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.CharField(choices=[('smartphone', 'Smartphone'), ('hardware', 'Hardware'), ('periferico', 'Perifericos'), ('game', 'Games'), ('eletrodomestico', 'Eletrodomesticos'), ('tv', 'TV')], max_length=16),
        ),
    ]
