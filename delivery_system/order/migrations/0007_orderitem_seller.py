# Generated by Django 3.2 on 2021-04-24 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210424_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='seller',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
