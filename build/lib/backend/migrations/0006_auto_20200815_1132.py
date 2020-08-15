# Generated by Django 3.0.8 on 2020-08-15 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_bookchapter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookitem',
            name='count',
        ),
        migrations.AddField(
            model_name='bookchapter',
            name='load',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookchapter',
            name='name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bookitem',
            name='url',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
