# Generated by Django 4.2.3 on 2023-08-17 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bot', '0003_alter_masterconversation_prompt_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterconversation',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
