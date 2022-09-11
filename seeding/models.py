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
