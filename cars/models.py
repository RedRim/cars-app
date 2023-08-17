from account.models import CustomUser

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from transliterate import translit

class Post(models.Model):
    title = models.CharField(max_length=75, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=False, verbose_name="Публикация")
    brand = models.ForeignKey('Brands', on_delete=models.PROTECT, verbose_name="Марка")
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Автор", null=True)
    users_like = models.ManyToManyField(CustomUser, related_name='images_liked', blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    def create(self, *args, **kwargs):
        self.time_create = timezone.now
        self.time_update = timezone.now
        super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(translit(self.title, reversed=True))
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            self.time_update = timezone.now
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['time_create']),
            models.Index(fields=['is_published'])
        ]
    
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

class FeedbackMessage(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Автор", null=True)
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
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name="Автор", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    content = models.TextField(blank=False, verbose_name="Комментарий", null=True)
    post = models.ForeignKey('Post', verbose_name="Комментарии", blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create', 'content']
