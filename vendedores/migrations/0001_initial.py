# Generated by Django 4.2.6 on 2024-01-25 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='logos')),
                ('nome', models.CharField(max_length=200)),
                ('contato', models.PositiveIntegerField()),
                ('endereco_numero', models.PositiveIntegerField()),
                ('endereco_rua', models.CharField(max_length=100)),
                ('endereco_bairro', models.CharField(max_length=50)),
                ('endereco_cidade', models.CharField(max_length=50)),
                ('endereco_estado', models.CharField(max_length=50)),
                ('endereco_estado_sigla', models.CharField(max_length=2)),
            ],
        ),
    ]