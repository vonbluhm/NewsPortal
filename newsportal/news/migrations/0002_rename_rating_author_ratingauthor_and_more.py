# Generated by Django 4.1.1 on 2022-09-11 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='rating',
            new_name='rating_author',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='postAuthor',
        ),
    ]
