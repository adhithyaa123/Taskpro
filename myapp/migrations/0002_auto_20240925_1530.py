# Generated by Django 3.2.25 on 2024-09-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
