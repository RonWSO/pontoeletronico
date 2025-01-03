# Generated by Django 5.1.4 on 2024-12-29 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255, unique=True)),
                ('endereco', models.CharField(max_length=255)),
                ('telefone', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('usuario', models.CharField(max_length=255, unique=True)),
                ('senha', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(db_index=True, max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ponto.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('inicio_expediente', models.TimeField()),
                ('fim_expediente', models.TimeField()),
                ('tempo_intervalo', models.IntegerField(default=60)),
                ('funcionario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ponto.funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Ponto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('entrada_expediente', models.TimeField()),
                ('saida_expediente', models.TimeField(blank=True, null=True)),
                ('inicio_intervalo', models.TimeField(blank=True, null=True)),
                ('saida_intervalo', models.TimeField(blank=True, null=True)),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ponto.funcionario')),
            ],
        ),
    ]
