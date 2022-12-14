# Generated by Django 4.1.1 on 2022-09-11 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seeding', '0002_alter_vegetable_options_alter_vegetable_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VegetableSort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Сорт овощей')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('distanceBetweenRows', models.IntegerField(verbose_name='Дистанция между рядов')),
                ('distanceBetweenBushes', models.IntegerField(verbose_name='Дистанция между кустов')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Сорт овоща',
                'verbose_name_plural': 'Сорта овощей',
                'ordering': ['time_create', 'name'],
            },
        ),
    ]
