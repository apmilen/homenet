# Generated by Django 2.2.1 on 2019-05-09 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('penny', '0004_user_user_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Availability',
        ),
    ]