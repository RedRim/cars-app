# Generated by Django 4.2.2 on 2023-07-15 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['time_create'], name='cars_post_time_cr_3b651b_idx'),
        ),
    ]
