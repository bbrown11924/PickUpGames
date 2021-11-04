# Generated by Django 3.2.8 on 2021-11-04 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pickup', '0005_merge_20211103_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='reciever',
        ),
        migrations.AddField(
            model_name='messages',
            name='receiver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='receiver', to='pickup.player'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='sender', to='pickup.player'),
        ),
    ]
