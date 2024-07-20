from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название города')
    country = models.CharField(max_length=100, db_index=True, verbose_name='Название страны')
    count = models.IntegerField(verbose_name='Количество поисков')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'