# Generated by Django 2.1.15 on 2024-09-23 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cidades', '0002_auto_20240923_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='estado',
            name='uf',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
