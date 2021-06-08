# Generated by Django 2.2.9 on 2021-04-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_delete_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
            ],
        ),
    ]
