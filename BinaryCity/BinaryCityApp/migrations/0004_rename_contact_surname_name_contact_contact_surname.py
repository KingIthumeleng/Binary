# Generated by Django 5.1.1 on 2024-09-23 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BinaryCityApp', '0003_contact_contact_surname_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='contact_surname_name',
            new_name='contact_surname',
        ),
    ]
