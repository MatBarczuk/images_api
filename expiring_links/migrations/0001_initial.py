# Generated by Django 3.2.5 on 2021-07-29 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpiringLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('token', models.UUIDField()),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
    ]
