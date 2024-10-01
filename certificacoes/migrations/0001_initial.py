# Generated by Django 5.0.9 on 2024-10-01 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=255)),
                ('siglaCertificador', models.CharField(max_length=3)),
                ('inativo', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'tb_certificador',
            },
        ),
        migrations.CreateModel(
            name='Certificacao',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('descricao', models.TextField()),
                ('siglaExame', models.CharField(max_length=50)),
                ('duracao', models.IntegerField()),
                ('observacao', models.TextField(blank=True, null=True)),
                ('inativo', models.BooleanField(default=False)),
                ('idCertificador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificacoes.certificador')),
            ],
            options={
                'db_table': 'tb_certificacao',
            },
        ),
    ]
