# Generated by Django 4.0.5 on 2023-11-17 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('API_key', models.CharField(max_length=150)),
                ('url', models.CharField(max_length=150)),
            ],
        ),
    ]
