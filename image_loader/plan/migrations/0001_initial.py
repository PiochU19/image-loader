# Generated by Django 3.2.3 on 2021-05-17 17:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(max_length=20)),
                ('allowed_sizes', models.CharField(default='200', max_length=255)),
                ('ability_to_expiring_links', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]