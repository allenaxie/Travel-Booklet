# Generated by Django 3.2.9 on 2022-01-20 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Trip Name')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('departure_location', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=400)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
