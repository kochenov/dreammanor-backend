from django.db import models


class Vegetable(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название овощей')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Овощ'
        verbose_name_plural = 'Овощи'
        ordering = ['time_create', 'name']


class VegetableSort(models.Model):
    name = models.CharField(max_length=255, verbose_name='Сорт овощей', db_index=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    distanceBetweenRows = models.PositiveIntegerField(verbose_name='Дистанция меж рядов')
    distanceBetweenBushes = models.PositiveIntegerField(verbose_name='Дистанция меж кустов')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    vegetable = models.ForeignKey('Vegetable', on_delete=models.PROTECT, null=True, verbose_name='Овощи')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сорт'
        verbose_name_plural = 'Сорт овощей'
        ordering = ['time_create', 'name']
