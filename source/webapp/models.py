from django.db import models


class Goal(models.Model):
    summary = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ForeignKey('webapp.Status', related_name='statuses',
                               on_delete=models.PROTECT, verbose_name='Статус')
    type = models.ManyToManyField('webapp.Type', related_name='goals', through='webapp.GoalType',
                                  through_fields=('goal', 'type'), blank=True, verbose_name='Тип')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return f'{self.summary}, {self.status}, {self.type}'

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


class GoalType(models.Model):
    goal = models.ForeignKey('webapp.Goal', related_name='goal_tags',
                             on_delete=models.CASCADE, verbose_name='Задача')
    type = models.ForeignKey('webapp.Type', related_name='type_goals',
                             on_delete=models.CASCADE, verbose_name='Тип')

    def __str__(self):
        return "{} | {}".format(self.goal, self.type)
