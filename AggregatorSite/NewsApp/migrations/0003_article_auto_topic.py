# Generated by Django 5.2.1 on 2025-06-03 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsApp', '0002_article_processed_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='auto_topic',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
