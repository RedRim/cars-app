from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Модель")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    short_content = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")
    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, verbose_name="Марка")
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, verbose_name="Автор", null=True)
    comments = models.ManyToManyField('Comment', verbose_name="Комментарии", blank=True)
    likes_amount = models.IntegerField(verbose_name="Лайки", default = 0)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def increase_like_amount(self):
        self.likes_amount += 1
        return self.likes_amount
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['time_create']
    
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
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True, null=True)
    is_moder = models.BooleanField(default=False)

    def get_default_photo():
        return 'photos/profile_picture/defaultphoto.jpg'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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

class Comment(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey('CustomUser', on_delete=models.PROTECT, verbose_name="Автор", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    content = models.TextField(blank=True, verbose_name="Комментарий", null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['time_create', 'content']
