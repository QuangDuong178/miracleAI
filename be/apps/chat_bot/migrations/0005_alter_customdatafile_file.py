# Generated by Django 4.2.3 on 2023-08-21 01:56

import apps.chat_bot.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bot', '0004_masterconversation_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customdatafile',
            name='file',
            field=models.FileField(upload_to=apps.chat_bot.models.pdf_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'txt'])]),
        ),
    ]