# Generated by Django 3.2.9 on 2021-12-06 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=500)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='episode',
            name='podcast_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcasts.feedchannel'),
        ),
    ]