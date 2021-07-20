from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import phone_regex, image_validator


class UserManager(BaseUserManager):
    """
    Менеджер пользователя (Модель)
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        База создания пользователя
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создание пользователя
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создание суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class School(models.Model):
    """
    Школа (Модель)
    """
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

    def __str__(self):
        return self.name


class Faculty(models.Model):
    """
    Факультет (Модель)
    """
    name = models.CharField('Название', max_length=100)
    school = models.ForeignKey(School, models.CASCADE, verbose_name='Школа')

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.name


# Custom User Class
class User(AbstractUser):
    """
    Пользователь (Модель)
    """
    class EducationChoices(models.TextChoices):
        """
         Уроаень образования
        """
        BACHELOR = 'bachelor', 'Бакалавриат'
        SPECIALTY = 'specialty', 'Специалитет'
        MAGISTRACY = 'magistracy', 'Магистратура'
        GRADUATE_SCHOOL = 'graduate_school', 'Аспирантура'
        OTHER = 'other', 'Другое'

    username = None
    email = models.EmailField('Email', unique=True)
    image = models.ImageField('Аватар пользователя', blank=True, validators=[image_validator])
    name = models.CharField('Имя', max_length=256, default='', blank=True)
    surname = models.CharField('Фамилия', max_length=256, default='', blank=True)
    fathers_name = models.CharField('Отчество', max_length=256, default='', blank=True)
    education_level = models.CharField('Статус', max_length=20, choices=EducationChoices.choices,
                                       default=EducationChoices.BACHELOR)
    school = models.ForeignKey(School,verbose_name='Школа',null=True,blank=True,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty,verbose_name='Факультет',null=True,blank=True,on_delete=models.CASCADE)
    education_year = models.CharField('Год обучения', max_length=256, default='', blank=True)
    phone = models.CharField('мобильный телефон', max_length=256, validators=[phone_regex], blank=True)
    social_1 = models.URLField('ссылка на соц.сеть 1', default='', blank=True)
    social_2 = models.URLField('ссылка на соц.сеть 2', default='', blank=True)
    social_3 = models.URLField('ссылка на соц.сеть 3', default='', blank=True)

    email_notification = models.BooleanField('email-уведомления', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'fathers_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Organization(models.Model):
    """
    Организация (Модель)
    """
    class StatusChoices(models.TextChoices):
        """
        Статус организации
        """
        NEW = 'new', 'Новая'
        VERIFY = 'verify', 'Верифицированная'
        DENIED = 'denied', 'Отказано'

    name = models.CharField('Название организации', max_length=64)
    image = models.ImageField('Аватар организации', blank=True, validators=[image_validator])
    description = models.TextField('Описание', default='', blank=True)
    mission = models.TextField('Миссия', default='', blank=True)
    motivation = models.TextField('Мотивировка', default='', blank=True)
    work_trajectory = models.TextField('Траектория работы', default='', blank=True)
    goal = models.TextField('Цель', default='', blank=True)
    members = models.ManyToManyField(User, verbose_name='участники организации', through='MembersInOrganization',
                                     blank=True)
    social_network_1 = models.URLField('ссылка на соцсеть 1', blank=True)
    social_network_2 = models.URLField('ссылка на соцсеть 2', blank=True)
    phone = models.CharField(max_length=256, validators=[phone_regex], blank=True)
    email = models.EmailField('email', blank=True)

    status = models.CharField('Статус', max_length=20, choices=StatusChoices.choices,
                              default=StatusChoices.NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


# Intermediate table for m2m field on organization model
class MembersInOrganization(models.Model):
    """
    Члены организации (Модель)
    """
    class RoleChoices(models.TextChoices):
        """
        Роль в организации
        """
        MEMBER = 'member', 'Член организации'
        LEADER = 'leader', 'Глава/исполняющий обязанности организации'
        ADMIN = 'admin', 'Админимтратор'

    user = models.ForeignKey(User, models.CASCADE, verbose_name='пользователь')
    organization = models.ForeignKey(Organization, models.CASCADE, verbose_name='организация')
    role = models.CharField('роль в организации', max_length=10, choices=RoleChoices.choices,
                            default=RoleChoices.MEMBER)

    organization_confirm = models.BooleanField('Подтверждение организации', default=False)
    user_confirm = models.BooleanField('Подтверждение пользователя', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Член организации'
        verbose_name_plural = 'Члены организации'
        constraints = [
            models.UniqueConstraint(fields=['user', 'organization'], name='unique_member_in_organization')
        ]


class EventCategory(models.Model):
    """
    Категория мероприятия (Модель)
    """
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Категория события'
        verbose_name_plural = 'Категории событий'

    def __str__(self):
        return self.name


class EventType(models.Model):
    """
    Тип мероприятия (Модель)
    """
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Тип события'
        verbose_name_plural = 'Типы событий'

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Мероприятие (Модель)
    """
    class LevelChoices(models.TextChoices):
        """
        Уровень мероприятия
        """
        INTERNATIONAL = 'international', 'Международный'
        COUNTRY = 'country', 'Всероссийский'
        REGIONAL = 'regional', 'Региональный'
        UNIVERSITY = 'university', 'Университетский'

    class StatusChoices(models.TextChoices):
        """
        Статус мероприятия
        """
        NEW = 'new', 'Новое'
        IN_RELEASE = 'in_release', 'В релизе'
        VERIFY = 'verify', 'Верифицированное'
        DENIED = 'denied', 'Отказано'

    name = models.CharField('Название мероприятия', max_length=64)
    image = models.ImageField('Картинка мероприятия', blank=True, validators=[image_validator])
    organization = models.ForeignKey(Organization, verbose_name="Организатор мероприятия", on_delete=models.CASCADE)
    time = models.TimeField('Время проведения')
    auditorium = models.CharField('Место проведения/Аудитория', max_length=64)
    organizers = models.ManyToManyField(User, verbose_name='Организаторы мероприятия', through='EventOrganizers',
                                        blank=True)
    date = models.DateField('Дата проведения')
    date_end = models.DateField('Дата окончания')
    level = models.CharField('Уровень мероприятия', max_length=64, choices=LevelChoices.choices,
                             default=LevelChoices.UNIVERSITY)
    guests = models.ManyToManyField(User, verbose_name='Участники мероприятия', related_name='guests', blank=True)

    status = models.CharField('Статус', max_length=64, choices=StatusChoices.choices,
                              default=StatusChoices.NEW)

    event_category = models.ManyToManyField(EventCategory, verbose_name='Категории мероприятия',related_name='event_category',blank=True)
    event_type = models.ManyToManyField(EventType, verbose_name='Типы мероприятия',related_name='event_type',blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

    def __str__(self):
        return self.name


# Intermediate table on m2m field in Event model
class EventOrganizers(models.Model):
    """
    Организаторы мероприятия (Модель)
    """
    class RoleChoices(models.TextChoices):
        """
        Роль в мероприятии
        """
        LEADER = 'leader', 'Руководитель'
        MANAGER = 'manager', 'Организатор'
        EXECUTOR = 'executor', 'Исполнитель'
        VOLUNTEER = 'volunteer', 'волонтер'

    user = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name='Мероприятие', on_delete=models.CASCADE)
    role = models.CharField('Роль участника', max_length=64, blank=True, null=True, choices=RoleChoices.choices,
                            default=RoleChoices.VOLUNTEER)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Организатор мероприятия'
        verbose_name_plural = 'Организаторы мероприятий'
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_organizers_in_event')
        ]


class EventGuests(models.Model):
    """
    Посетители мероприятия (Модель)
    """
    user = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name='Мероприятие', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Гость мероприятия'
        verbose_name_plural = 'Гости мероприятий'
        constraints = [
            models.UniqueConstraint(fields=['user', 'event'], name='unique_guest_in_event')
        ]


class Notification(models.Model):
    """
    Уведомление (Модель)
    """
    user = models.ForeignKey(User, verbose_name='Участник', on_delete=models.CASCADE)
    message = models.TextField('Уведомление')
    link = models.CharField('Ссылка', max_length=250)
    viewed = models.BooleanField('Просмотренно', default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'


class Slide(models.Model):
    """
    Слайд (Модель)
    """
    name = models.CharField('Название', max_length=100)
    img = models.ImageField('Изображение', max_length=100)
    link = models.CharField('Ссылка', max_length=250)

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

    def __str__(self):
        return self.name


