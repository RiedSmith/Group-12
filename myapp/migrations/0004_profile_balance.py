# Generated by Django 3.2.12 on 2023-04-17 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_delete_shoppingcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]
