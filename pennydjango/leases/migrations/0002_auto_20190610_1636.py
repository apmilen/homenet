# Generated by Django 2.2.1 on 2019-06-10 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lease',
            name='op_received_at',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='MoveInCost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('charge', models.CharField(max_length=255)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leases.Lease')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaseMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=155)),
                ('email', models.CharField(max_length=255)),
                ('applicant_type', models.CharField(max_length=155)),
                ('app_fee', models.DecimalField(decimal_places=2, default=100, max_digits=15)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leases.Lease')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
