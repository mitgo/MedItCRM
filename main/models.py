from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
class MainMenu(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название')
    app_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Ссылка')
    icon = models.CharField(max_length=100, null=True, blank=True, verbose_name='Иконка')
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, db_index=True, related_name='children', verbose_name='Родитель')
    position = models.IntegerField(null=True, blank=True, verbose_name='Позиция')
    user = models.ManyToManyField(User, verbose_name='Пользователи', blank=True, related_name="users")
    group = models.ManyToManyField(Group, verbose_name='Группы', blank=True, related_name="groups")

    class MPTTMeta:
        OrderInsertionBy = ['position', 'title']

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def submenus(self):
        return self.children

    def __str__(self):
        return self.title

