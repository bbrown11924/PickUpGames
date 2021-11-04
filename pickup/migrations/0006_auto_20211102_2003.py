# Generated by Django 3.2.8 on 2021-11-03 00:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pickup', '0005_merge_0003_auto_20211028_2113_0004_auto_20211025_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(choices=[(0, '12:00 AM'), (1, '12:15 AM'), (2, '12:30 AM'), (3, '12:45 AM'), (4, '01:00 AM'), (5, '01:15 AM'), (6, '01:30 AM'), (7, '01:45 AM'), (8, '02:00 AM'), (9, '02:15 AM'), (10, '02:30 AM'), (11, '02:45 AM'), (12, '03:00 AM'), (13, '03:15 AM'), (14, '03:30 AM'), (15, '03:45 AM'), (16, '04:00 AM'), (17, '04:15 AM'), (18, '04:30 AM'), (19, '04:45 AM'), (20, '05:00 AM'), (21, '05:15 AM'), (22, '05:30 AM'), (23, '05:45 AM'), (24, '06:00 AM'), (25, '06:15 AM'), (26, '06:30 AM'), (27, '06:45 AM'), (28, '07:00 AM'), (29, '07:15 AM'), (30, '07:30 AM'), (31, '07:45 AM'), (32, '08:00 AM'), (33, '08:15 AM'), (34, '08:30 AM'), (35, '08:45 AM'), (36, '09:00 AM'), (37, '09:15 AM'), (38, '09:30 AM'), (39, '09:45 AM'), (40, '10:00 AM'), (41, '10:15 AM'), (42, '10:30 AM'), (43, '10:45 AM'), (44, '11:00 AM'), (45, '11:15 AM'), (46, '11:30 AM'), (47, '11:45 AM'), (48, '12:00 PM'), (49, '12:15 PM'), (50, '12:30 PM'), (51, '12:45 PM'), (52, '01:00 PM'), (53, '01:15 PM'), (54, '01:30 PM'), (55, '01:45 PM'), (56, '02:00 PM'), (57, '02:15 PM'), (58, '02:30 PM'), (59, '02:45 PM'), (60, '03:00 PM'), (61, '03:15 PM'), (62, '03:30 PM'), (63, '03:45 PM'), (64, '04:00 PM'), (65, '04:15 PM'), (66, '04:30 PM'), (67, '04:45 PM'), (68, '05:00 PM'), (69, '05:15 PM'), (70, '05:30 PM'), (71, '05:45 PM'), (72, '06:00 PM'), (73, '06:15 PM'), (74, '06:30 PM'), (75, '06:45 PM'), (76, '07:00 PM'), (77, '07:15 PM'), (78, '07:30 PM'), (79, '07:45 PM'), (80, '08:00 PM'), (81, '08:15 PM'), (82, '08:30 PM'), (83, '08:45 PM'), (84, '09:00 PM'), (85, '09:15 PM'), (86, '09:30 PM'), (87, '09:45 PM'), (88, '10:00 PM'), (89, '10:15 PM'), (90, '10:30 PM'), (91, '10:45 PM'), (92, '11:00 PM'), (93, '11:15 PM'), (94, '11:30 PM'), (95, '11:45 PM')])),
                ('park', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='pickup.parks')),
                ('player', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='schedule',
            constraint=models.UniqueConstraint(fields=('player', 'park', 'time'), name='pickup_schedule_unique'),
        ),
    ]