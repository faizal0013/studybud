# Generated by Django 4.1.2 on 2022-10-21 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='update',
            new_name='updated',
        ),
    ]