# Generated by Django 5.1.1 on 2024-09-23 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BinaryCityApp', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contact_surname_name',
            field=models.CharField(default='Surname', max_length=255),
        ),
    ]
