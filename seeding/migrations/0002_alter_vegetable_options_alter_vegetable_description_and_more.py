# Generated by Django 4.1.1 on 2022-09-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeding', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vegetable',
            options={'ordering': ['time_create', 'name'], 'verbose_name': 'Овощ', 'verbose_name_plural': 'Овощи'},
        ),
        migrations.AlterField(
            model_name='vegetable',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vegetable',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название овощей'),
        ),
        migrations.AlterField(
            model_name='vegetable',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='vegetable',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
