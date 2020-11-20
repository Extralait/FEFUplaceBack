from django.db import models


class Organization(models.Model):
    name = models.CharField('Название организации', max_length=64)
    description = models.TextField('Описание')
    mission = models.TextField('Миссия')
    motivation = models.TextField('Мотивировка')
    work_trajectory = models.TextField('Траектория работы')
    goal = models.TextField('Цель')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Название мероприятия', max_length=64)
    organization = models.ForeignKey(Organization, verbose_name="Организатор мероприятия")
    date = models.DateField('Дата проведения')

    def __str__(self):
        return self.name


class Inventory(models.Model):
    name = models.CharField('Название инвентаря', max_length=64)
    description = models.TextField('Описание предмета инвентаря')
    availability = models.BooleanField('доступность')
