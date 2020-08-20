from django.db import migrations


def add_transit_options(apps, schema_editor):
    from listings.constants import TRANSIT_OPTIONS
    TransitOptions = apps.get_model("listings", "TransitOptions")
    for line in TRANSIT_OPTIONS:
        TransitOptions.objects.create(name=line[0])


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0018_auto_20200820_2051')
    ]

    operations = [
        migrations.RunPython(add_transit_options)
    ]
