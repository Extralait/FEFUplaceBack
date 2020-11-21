from django.db import models


class Organization(models.Model):
    name = models.CharField('Название организации', max_length=64)
    description = models.TextField('Описание')
    mission = models.TextField('Миссия')
    motivation = models.TextField('Мотивировка')
    work_trajectory = models.TextField('Траектория работы')
    goal = models.TextField('Цель')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Название мероприятия', max_length=64)
    organization = models.ManyToManyField(Organization, verbose_name="Организатор мероприятия")
    date = models.DateField('Дата проведения')

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField('Название инвентаря', max_length=64)
    description = models.TextField('Описание предмета инвентаря')
    availability = models.BooleanField('доступность')

    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентарь'

    def __str__(self):
        return self.name
