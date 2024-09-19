# Generated by Django 2.1.15 on 2024-09-19 22:25

from django.db import migrations, models
import django.db.models.deletion

def update_aluno_nome_to_uppercase(apps, schema_editor):
    Aluno = apps.get_model('alunos', 'Aluno')
    for aluno in Aluno.objects.all():
        aluno.nome = aluno.nome.upper()  # Transforma o nome em caixa alta
        aluno.save()


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0002_auto_20240919_1812'),
    ]

    operations = [
        migrations.RunPython(update_aluno_nome_to_uppercase),
    ]
