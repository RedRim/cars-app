# Generated by Django 4.2.2 on 2023-08-15 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0009_alter_post_users_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='short_content',
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=75, verbose_name='Заголовок'),
        ),
    ]
