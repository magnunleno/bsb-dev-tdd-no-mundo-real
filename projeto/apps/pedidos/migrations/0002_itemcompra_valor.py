# Generated by Django 2.0.9 on 2018-11-05 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemcompra',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]
