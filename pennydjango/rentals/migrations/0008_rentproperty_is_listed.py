# Generated by Django 2.2.1 on 2019-05-03 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0007_auto_20190430_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentproperty',
            name='is_listed',
            field=models.BooleanField(default=True),
        ),
    ]
