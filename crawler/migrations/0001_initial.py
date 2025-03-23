# Generated by Django 5.1.6 on 2025-03-14 16:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleSearchConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=255)),
                ('results', models.IntegerField()),
                ('safe', models.CharField(max_length=30)),
                ('lang', models.CharField(blank=True, max_length=4, null=True)),
                ('region', models.CharField(blank=True, max_length=4, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleSearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('crawled_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_results', to='crawler.googlesearchconfig')),
            ],
        ),
    ]
