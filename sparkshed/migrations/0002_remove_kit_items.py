# Generated by Django 4.1.1 on 2022-09-24 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sparkshed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit',
            name='items',
        ),
    ]