# Generated by Django 4.2 on 2023-04-22 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myFirstApp', '0009_quote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quote',
            name='text',
        ),
        migrations.AddField(
            model_name='quote',
            name='quote',
            field=models.TextField(blank=True, null=True),
        ),
    ]
