# Generated by Django 3.2 on 2023-07-08 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statuehistory',
            name='lead',
        ),
        migrations.DeleteModel(
            name='Lead',
        ),
        migrations.DeleteModel(
            name='StatueHistory',
        ),
    ]
