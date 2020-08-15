from django.db import models
from django.core.validators import MaxLengthValidator


class Goal(models.Model):
    summary = models.CharField(max_length=200, verbose_name='Заголовок',
                               validators=[MaxLengthValidator(20)])
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='statuses',
                               on_delete=models.PROTECT, verbose_name='Статус', default=1)
    type = models.ManyToManyField('webapp.Type', related_name='goals', blank=True, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return f'{self.summary}, {self.status}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
