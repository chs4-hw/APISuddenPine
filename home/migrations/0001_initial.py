# Generated by Django 3.0.5 on 2020-04-16 12:25

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
            name='RoomControl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomtype', models.CharField(max_length=50)),
                ('heating', models.DecimalField(decimal_places=1, max_digits=4)),
                ('light', models.BooleanField(default=False)),
                ('safetyalarm', models.BooleanField(default=False)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HomeStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dailyBattery', models.DecimalField(decimal_places=3, default=0, max_digits=7)),
                ('dailyConS', models.DecimalField(decimal_places=3, default=0, max_digits=7)),
                ('dailySave', models.DecimalField(decimal_places=3, default=0, max_digits=7)),
                ('dailySolar', models.DecimalField(decimal_places=3, default=0, max_digits=7)),
                ('updated', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('home', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=50)),
                ('deviceconsumption', models.DecimalField(decimal_places=3, max_digits=5)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DayLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dailyBattery', models.DecimalField(decimal_places=3, max_digits=9)),
                ('dailyConS', models.DecimalField(decimal_places=3, max_digits=9)),
                ('dailySave', models.DecimalField(decimal_places=3, max_digits=9)),
                ('dailySolar', models.DecimalField(decimal_places=3, max_digits=9)),
                ('date', models.DateField()),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]