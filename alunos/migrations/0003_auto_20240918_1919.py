# Generated by Django 2.1.15 on 2024-09-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0002_auto_20240918_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
