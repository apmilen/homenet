# Generated by Django 2.2.4 on 2020-07-23 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0012_auto_20200717_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='move_in_cost',
            field=models.CharField(choices=[('first_last_security', 'First, Last, and Security'), ('first_security', 'First and Security')], max_length=100),
        ),
    ]