# Generated by Django 2.2.10 on 2020-02-27 20:10

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
            name='MediaType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField()),
                ('deleted', models.BooleanField(default=False)),
                ('path', models.URLField()),
                ('_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_type', to='course.MediaType')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_classroom', to=settings.AUTH_USER_MODEL)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_providor', to='course.Provider')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_publisher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]