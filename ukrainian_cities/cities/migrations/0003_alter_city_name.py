# Generated by Django 3.2.9 on 2021-12-31 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_auto_20211221_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.TextField(primary_key=True, serialize=False, verbose_name='name'),
        ),
    ]
