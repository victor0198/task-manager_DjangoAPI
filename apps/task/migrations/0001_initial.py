# Generated by Django 2.2.1 on 2019-05-27 10:11

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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('created', 'created'), ('inprocess', 'inprocess'), ('finished', 'finished')], default='created', max_length=10)),
                ('date_create_task', models.DateTimeField(blank=True, null=True)),
                ('update_task', models.DateTimeField(blank=True, null=True)),
                ('user_assigned', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_assign', to=settings.AUTH_USER_MODEL)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_creat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
