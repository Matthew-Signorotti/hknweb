# Generated by Django 2.1.3 on 2018-11-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alumnus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perm_email', models.EmailField(max_length=254)),
                ('mailing_list', models.BooleanField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]