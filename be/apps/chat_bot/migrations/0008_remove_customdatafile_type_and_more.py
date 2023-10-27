# Generated by Django 4.2.3 on 2023-09-26 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_bot', '0007_customdatafile_type_masterconversation_refer_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customdatafile',
            name='type',
        ),
        migrations.AddField(
            model_name='customdatafile',
            name='display_refer_type',
            field=models.CharField(choices=[('1', 'File + Page'), ('2', 'File Only'), ('3', 'No Display')], default=1, max_length=20),
        ),
    ]
