# Generated by Django 2.2.4 on 2020-07-29 00:12

from django.db import migrations, models
import penny.utils


class Migration(migrations.Migration):

    dependencies = [
        ('leases', '0011_auto_20200723_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalapplication',
            name='id_file',
            field=models.FileField(null=True, upload_to=penny.utils.rental_doc_path, validators=[penny.utils.validate_file_size], verbose_name='ID'),
        ),
    ]