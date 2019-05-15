from django.db import migrations


def add_amenities(apps, schema_editor):
    from listings.constants import AMENITIES
    Amenity = apps.get_model("listings", "Amenity")
    for group in AMENITIES:
        for amenity in group:
            Amenity.objects.create(name=amenity[0])


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_amenities)
    ]
