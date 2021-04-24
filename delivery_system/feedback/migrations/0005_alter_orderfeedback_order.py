# Generated by Django 3.2 on 2021-04-24 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210424_1142'),
        ('feedback', '0004_auto_20210424_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderfeedback',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_orders', to='order.order'),
        ),
    ]