from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse

class Cars(models.Model):
    title = models.CharField(max_length=255, verbose_name="Модель")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    short_content = models.CharField(max_length=255, verbose_name="Краткое описание")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")
    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, verbose_name="Марка")
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, verbose_name="Автор", null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статьи про машины'
        verbose_name_plural = 'Статьи про машины'
        ordering = ['time_create', 'brand_id']
    
class Brands(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('brand', kwargs={'brand_slug':self.slug})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'
        ordering = ['id']

def get_default_photo():
    return 'cars/static/cars/images/default_photo.avif'
    
class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="user URL")
    photo = models.ImageField(upload_to="photos/profile_picture", verbose_name="Фото", blank=True, null=True)
    is_moder = models.BooleanField(default=False)

    def get_default_photo():
        return 'cars/static/cars/images/default_photo.avif'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username 
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug':self.slug})
    
class FeedbackMessage(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, verbose_name="Автор", null=True)
    short_content = models.CharField(max_length=50, verbose_name="Краткое описание")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    content = models.TextField(blank=True, verbose_name="Текст обращения")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['time_create', 'author_id']
