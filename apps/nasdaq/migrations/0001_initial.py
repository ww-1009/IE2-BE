# Generated by Django 3.2.5 on 2021-10-30 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NasdaqIndex3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField(blank=True, null=True)),
                ('index', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'nasdaq_index_3',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NasdaqIndex5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(blank=True, max_length=255, null=True)),
                ('prompt', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nasdaq_index_5',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NasdaqIndex7',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(blank=True, max_length=255, null=True)),
                ('prompt', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'nasdaq_index_7',
                'managed': False,
            },
        ),
    ]