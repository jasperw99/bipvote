# Generated by Django 4.0.4 on 2022-04-26 16:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_voteopinion_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='voteopinion',
            name='vote_opinion',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.DeleteModel(
            name='Counts',
        ),
    ]
