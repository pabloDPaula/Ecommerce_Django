# Generated by Django 4.1 on 2022-12-03 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0007_remove_produto_descricao_curta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='produto',
            name='informacao_tecnica',
            field=models.TextField(),
        ),
    ]
