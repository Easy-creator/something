# Generated by Django 4.2.7 on 2024-02-22 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0003_passphrase_amount_of_pi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passphrase',
            name='keys',
            field=models.TextField(max_length=200, unique=True),
        ),
    ]
