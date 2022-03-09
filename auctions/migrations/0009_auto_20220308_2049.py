# Generated by Django 3.2 on 2022-03-08 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20220308_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_desc',
            field=models.CharField(max_length=300),
        ),
    ]