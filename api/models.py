from django.db import models
from django.db.models.base import Model
import datetime

# Create your models here.

class User(models.Model):
    negative = [('да', 'да'), ('нет', 'нет')]
    name = models.CharField('Имя', max_length=45)
    surename = models.CharField('Фамилия', max_length=45, default='')
    patronymic = models.CharField('Отчество', max_length=45, default='', blank=True)
    email = models.CharField('Email', max_length=45)
    phone = models.CharField('Телефон', max_length=45, blank=True)
    note = models.TextField('Примечания', max_length=255, blank=True)
    verify = models.CharField("Верификация", null=True, default='complete', max_length=45)
    log_in = models.BooleanField("Пользователь авторизован", default=False)

    class Meta:
        abstract = True

    def getFIO(self):
        pat = ''
        try: pat = f'{self.patronymic[0]}.'
        except: pass
        return f'{self.surename} {self.name[0]}. {pat}'

    def __str__(self):
        return self.getFIO()

    


class Tutor(User):
    admin = models.CharField('Статус администратора', choices=User.negative, max_length=45, blank=True)
    specialist = models.CharField('Специалист УПО', choices=User.negative, max_length=45,  blank=True)
    login =  models.CharField('Логин', max_length=45, default=None)
    password =  models.CharField('Пароль', max_length=45, default=None)
    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководители"


class Group(models.Model):
    name = models.CharField('Имя группы', max_length=45)
    leader = models.ForeignKey(Tutor, null=True, on_delete=models.SET_NULL)
    year = models.CharField('Год формирования', max_length=45)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self) -> str:
        return f'{self.name} Руководитель: {self.leader}'


class Student(User):
    gender_list = [('м','м'), ('ж', 'ж')]
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    parentsArePensioners = models.CharField('Родители пенсионеры', choices=User.negative, max_length=45, default='нет', blank=True)
    amountOfChildren = models.IntegerField("Количество детей", default=0, blank=True)
    dateOfBirth = models.DateField("День рождения")
    cityOfRegistration = models.CharField('Город прописки', max_length=45)
    cityOfResidence = models.CharField('Город проживания', max_length=45)
    gender = models.CharField('Гендер', max_length=2, choices=gender_list, default='м')
    juvenileAffairsUnit = models.CharField('Отдел по делам несовершеннолетних', max_length=45, choices=User.negative, default='нет', blank=True)
    fullFamily = models.CharField('Состав семьи', max_length=45, blank=True)
    interests = models.TextField('Интересы', max_length=255, blank=True)
    sportsSections = models.CharField('Спортивные секции', max_length=45, blank=True)

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def getStrfedDate(self):
        return datetime.datetime.strftime(self.dateOfBirth, '%Y-%m-%d')



class Parent(User):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    who = models.CharField('Кем приходится', max_length=45, blank=True)

    class Meta:
        verbose_name = "Родитель"
        verbose_name_plural = "Родители"


