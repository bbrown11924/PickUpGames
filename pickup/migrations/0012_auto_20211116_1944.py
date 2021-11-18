# Generated by Django 3.2.8 on 2021-11-17 00:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pickup', '0011_player_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSignup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='schedule',
            name='pickup_schedule_unique',
        ),
        migrations.RenameField(
            model_name='schedule',
            old_name='player',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='schedule',
            name='name',
            field=models.CharField(default='', max_length=400),
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('park', 'time', 'date'), name='pickup_schedule_unique'),
        ),
        migrations.AddField(
            model_name='eventsignup',
            name='event',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='pickup.schedule'),
        ),
        migrations.AddField(
            model_name='eventsignup',
            name='player',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='eventsignup',
            constraint=models.UniqueConstraint(fields=('player', 'event'), name='pickup_eventsignup_unique'),
        ),
    ]