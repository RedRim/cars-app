# Generated by Django 4.2.2 on 2023-06-25 04:45

import cars.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'ordering': ['id'], 'verbose_name': 'Марка автомобиля', 'verbose_name_plural': 'Марки автомобилей'},
        ),
        migrations.AlterModelOptions(
            name='cars',
            options={'ordering': ['time_create', 'brand_id'], 'verbose_name': 'Статьи про машины', 'verbose_name_plural': 'Статьи про машины'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_moder',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cars',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Публикация'),
        ),
        migrations.AlterField(
            model_name='cars',
            name='short_content',
            field=models.CharField(max_length=255, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(blank=True, default=cars.models.get_default_photo, upload_to='photos/profile_picture', verbose_name='Фото'),
        ),
        migrations.CreateModel(
            name='FeedbackMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_content', models.CharField(max_length=50, verbose_name='Краткое описание')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('content', models.TextField(blank=True, verbose_name='Текст обращения')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['time_create', 'author_id'],
            },
        ),
    ]
