# Generated by Django 3.2.3 on 2021-05-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_rename_plan_type_plan_plan_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='ability_to_expiring_links',
            new_name='ability_to_generate_expiring_links',
        ),
        migrations.AddField(
            model_name='plan',
            name='acces_to_the_og',
            field=models.BooleanField(default=False),
        ),
    ]
