# Generated by Django 3.2.5 on 2021-11-07 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nasdaq', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DasdaqDepth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(blank=True, db_collation='utf8_bin', max_length=255, null=True)),
                ('depth', models.CharField(blank=True, db_collation='utf8_bin', max_length=255, null=True)),
                ('name', models.CharField(blank=True, db_collation='utf8_bin', max_length=255, null=True)),
            ],
            options={
                'db_table': 'dasdaq_depth',
                'managed': False,
            },
        ),
    ]
