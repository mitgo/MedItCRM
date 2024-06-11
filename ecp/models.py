from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from pytils.translit import translify
import datetime
from django.contrib.auth.models import Permission


class CustomUserPermissions(Permission):
    class Meta:
        abstract = True
        permissions = (
            ("guest", "Can view only guest esign's data"),
            ("viewer", "Can view all esign's data"),
            ("manager", "Can to do everything")
        )


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DepartmentTypes(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Тип подразделений'
        verbose_name_plural = 'Типы подразделений'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Departments(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    type = models.ForeignKey(DepartmentTypes, null=True, verbose_name='Тип подразделения', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Отделение/Отдел'
        verbose_name_plural = 'Отделения/Отделы'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Decrees(models.Model):
    # @staticmethod
    def get_translitfilename(self, filename):
        _now = datetime.datetime.now()
        return f'uploads/decrees/{_now.strftime("%Y")}-{_now.strftime("%m")}/{translify(filename)}'
    number = models.IntegerField(verbose_name='Номер приказа')
    d_date = models.DateField(default=timezone.now, verbose_name='Дата приказа')
    file = models.FileField(upload_to=get_translitfilename, verbose_name='Файл приказа',
                            validators=[FileExtensionValidator(['pdf'])])

    class Meta:
        verbose_name = 'Приказ'
        verbose_name_plural = 'Приказы'
        ordering = ['d_date', 'number']

    def __str__(self):
        return F'{self.number}, {self.d_date}'


class Persons(models.Model):
    fam = models.CharField(max_length=40, verbose_name='Фамилия')
    im = models.CharField(max_length=40, verbose_name='Имя')
    ot = models.CharField(max_length=40, verbose_name='Отчество', null=True, blank=True)
    db = models.DateField(verbose_name='Дата рождения')
    bitrh_place = models.CharField(max_length=100, verbose_name='Место рождения')
    post = models.CharField(max_length=255, verbose_name='Должность', null=True)
    phone = models.CharField(max_length=12, verbose_name='Телефон для связи', null=True, blank=True)
    dep = models.ForeignKey(Departments, verbose_name='Отделение', on_delete=models.PROTECT)
    snils = models.CharField(max_length=11, verbose_name='СНИЛС')
    inn = models.CharField(max_length=12, verbose_name='ИНН')
    pasp_s = models.CharField(max_length=5, verbose_name='Серия паспорта')
    pasp_n = models.CharField(max_length=7, verbose_name='Номер паспорта')
    pasp_dep = models.CharField(max_length=7, verbose_name='Код подразделения')
    pasp_date = models.DateField(verbose_name='Дата выдачи паспорта')
    pasp_kem = models.CharField(max_length=255, verbose_name='Кем выдан паспорт')
    is_active = models.BooleanField(default=True, verbose_name='Активен?')
    decrees = models.ManyToManyField(Decrees, verbose_name='Приказы', blank=True, related_name="persons")

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['fam', 'im', 'ot', 'db']

    def __str__(self):
        return f' {self.fam} {self.im}'


# todo кто изготовил подпись???
class Esigns(models.Model):
    # @staticmethod
    def get_translitfilename(self, filename):
        _now = datetime.datetime.now()
        return f'uploads/certs/{_now.strftime("%Y")}-{_now.strftime("%m")}/{translify(filename)}'

    person = models.ForeignKey(Persons, verbose_name='Сотрудник', on_delete=models.PROTECT)
    request_num = models.CharField(max_length=6, verbose_name='Номер запроса')
    request_link = models.CharField(max_length=255, verbose_name='Ссылка на черновик')
    date_start = models.DateField(default=timezone.now, verbose_name='Дата создания черновика')
    date_get = models.DateField(null=True, verbose_name='Дата получения', blank=True)
    date_valid = models.DateField(null=True, verbose_name='Действует до', blank=True)
    key = models.CharField(null=True, max_length=100, verbose_name='Серийный номер сертификата', blank=True)
    cert = models.FileField(upload_to=get_translitfilename, null=True, blank=True, verbose_name='Файл сертификата',
                            validators=[FileExtensionValidator(['pfx', 'rar'])])
    cer = models.FileField(upload_to=get_translitfilename, null=True, blank=True, verbose_name='Сертификат CER',
                           validators=[FileExtensionValidator(['cer'])])
    note = models.TextField(null=True, blank=True, verbose_name='Примечание')

    class Meta:
        verbose_name = 'ЭЦП'
        verbose_name_plural = 'ЭЦПшки'
        ordering = ['date_start']

    def __str__(self):
        return f'{self.person} {self.date_valid}'


class EsignStatus(models.Model):
    esign = models.ForeignKey(Esigns, verbose_name='ЭЦП', on_delete=models.CASCADE)
    status_code = models.IntegerField(verbose_name='Код статуса')
    status_txt = models.CharField(max_length=100, verbose_name='Статус ЭЦП')
    reason = models.CharField(max_length=255, verbose_name='Причина', blank=True, null=True)
    link = models.CharField(max_length=255, verbose_name='Ссылка', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата установления статуса')

    class Meta:
        verbose_name = 'Статус ЭЦП'
        verbose_name_plural = 'Статусы ЭЦП'
        unique_together = ('esign', 'status_txt', 'reason', 'link')

    def __str__(self):
        return f'{self.status_txt} {self.date}'


class Settings(models.Model):
    setting_name = models.CharField(max_length=255, verbose_name='Наименование настройки')
    setting_value = models.CharField(max_length=255, verbose_name='Значение настройки')
    setting_description = models.CharField(max_length=255, verbose_name='Описание настройки')

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return f'{self.setting_name} - {self.setting_value}'
