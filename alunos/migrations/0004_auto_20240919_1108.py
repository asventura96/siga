# Generated by Django 2.1.15 on 2024-09-19 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0003_auto_20240918_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='cidade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
