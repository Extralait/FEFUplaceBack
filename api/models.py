from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'manager')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Custom User Class
class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        CLIENT = 'client', 'Клиент'
        MANAGER = 'manager', 'Менеджер'

    username = None
    full_name = models.CharField('ФИО', max_length=100)
    role = models.CharField('Роль пользователя', max_length=10, choices=RoleChoices.choices,
                            default=RoleChoices.CLIENT)
    mailing_address = models.CharField('Адрес доставки', max_length=100)
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name


class Organization(models.Model):
    name = models.CharField('Название организации', max_length=64)
    description = models.TextField('Описание')
    mission = models.TextField('Миссия')
    motivation = models.TextField('Мотивировка')
    work_trajectory = models.TextField('Траектория работы')
    goal = models.TextField('Цель')
    members = models.ManyToManyField(User, verbose_name='участники организации', through='MembersInOrganization')

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class MembersInOrganization(models.Model):
    class RoleChoices(models.TextChoices):
        MEMBER = 'member', 'Член организации'
        LEADER = 'leader', 'Глава/исполняющий обязанности организации'

    user = models.ForeignKey(User, models.CASCADE, verbose_name='пользователь')
    organization = models.ForeignKey(Organization, models.CASCADE, verbose_name='организация')
    role = models.CharField('роль в организации', max_length=10, choices=RoleChoices.choices,
                            default=RoleChoices.MEMBER)


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
