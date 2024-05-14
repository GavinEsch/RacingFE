# Generated by Django 5.0 on 2024-05-13 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeBoards', '0007_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaderboardentry',
            name='game',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='TimeBoards.game'),
            preserve_default=False,
        ),
    ]
