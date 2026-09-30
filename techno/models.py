from django.db import models
from account.models import User


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    title = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.title


class Characteristic(models.Model):
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    title = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'Техники'

    title = models.CharField('Название', max_length=50)
    image = models.ImageField('Изображение', upload_to='techno/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    characteristic = models.ManyToManyField('Characteristic', verbose_name='Характеристика')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title

    