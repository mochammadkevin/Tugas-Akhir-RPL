# Generated by Django 4.2 on 2023-04-20 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myFirstApp', '0007_remove_task_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
