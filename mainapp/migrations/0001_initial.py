# Generated by Django 4.0.6 on 2024-03-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='tipos_documento_identidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomenclatura', models.CharField(max_length=150, verbose_name='Nomenclatura')),
                ('nombre', models.CharField(max_length=350, verbose_name='Nombre')),
            ],
        ),
    ]
