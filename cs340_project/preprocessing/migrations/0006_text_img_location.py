# Generated by Django 3.2 on 2021-04-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preprocessing', '0005_alter_text_txt'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='img_location',
            field=models.CharField(default=None, max_length=100),
        ),
    ]