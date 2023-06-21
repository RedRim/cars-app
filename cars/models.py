from django.db import models
from django.urls import reverse

class Cars(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, null=True)
    characteristics = models.ForeignKey('Characteristics', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id':self.pk})
    
class Brands(models.Model):
    name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_id':self.pk})
    
class Characteristics(models.Model):
    year_release = models.IntegerField(verbose_name="Год выпуска")
    body_type = models.CharField(max_length=20, verbose_name="Тип кузова")
    engine_capacity = models.IntegerField(verbose_name="Объем двигателя")
    engine_power = models.IntegerField(verbose_name="Мощность двигателя")
    drive = models.CharField(max_length=20, verbose_name="Привод")
    fuel_consumption = models.IntegerField(verbose_name="Расход топлива")
    number_of_seats = models.IntegerField(verbose_name="Количество мест")
    trunk_volume = models.IntegerField(verbose_name="Объем багажника")
    cost = models.IntegerField(verbose_name="Стоимость")
