from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class ClientType(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип клиента'
        verbose_name_plural = 'Типы клиентов'


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено на',
                                      auto_now_add=True)
    full_name = models.CharField(max_length=255,
                                 verbose_name='Полное Имя')
    phone = models.CharField(max_length=255,
                             verbose_name='Телефон',
                             blank=True, null=True)
    phone_extra = models.CharField(max_length=255,
                                   verbose_name='Доп. телефон',
                                   blank=True, null=True)
    address = models.CharField(max_length=255,
                               verbose_name='Адрес')
    region = models.ForeignKey('Region',
                               on_delete=models.SET_NULL,
                               null=True, blank=True,
                               verbose_name='Регион')
    client_type = models.ForeignKey('ClientType',
                                    on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    verbose_name='Тип клиента')
    status = models.IntegerField(default=0,
                                 verbose_name='Статус')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клинет'
        verbose_name_plural = 'Клиенты'
