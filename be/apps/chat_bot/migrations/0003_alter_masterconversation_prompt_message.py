# Generated by Django 4.2.3 on 2023-08-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bot', '0002_masterconversation_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masterconversation',
            name='prompt_message',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
