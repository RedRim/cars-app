from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

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
            while CustomUser.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username 
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug':self.slug})
