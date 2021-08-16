# Generated by Django 3.2.1 on 2021-08-16 12:25

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=45), default=list, size=None)),
                ('source', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=45), default=list, size=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Preference',
                'verbose_name_plural': 'User Preferences',
                'db_table': 'user_preference',
            },
        ),
    ]
