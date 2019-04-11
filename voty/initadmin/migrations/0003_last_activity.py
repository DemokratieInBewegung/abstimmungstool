# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-03-30 18:15
from __future__ import unicode_literals
from django.db import migrations, models
from django.contrib.auth import get_user_model
from voty.initproc.models import Vote, Supporter, Like, Comment, Proposal, Pro, Contra, Moderation, Preference, Resistance
from voty.initadmin.models import UserConfig


def record_activity(config, datetime):
    config.last_activity = datetime if config.last_activity is None else max(config.last_activity, datetime)
    config.save()


def handle_model(model):
    for o in model.objects.all():
        if not (isinstance(o, Supporter) and o.initiative.state == 'p' and not o.ack):
            record_activity(o.user.config, o.changed_at if hasattr(o, 'changed_at') else o.created_at)


def init_last_activity(apps, schema_editor):
    for user in get_user_model().objects.all():
        UserConfig.objects.get_or_create(user=user)

    handle_model(Vote)
    handle_model(Supporter)
    handle_model(Like)
    handle_model(Comment)
    handle_model(Proposal)
    handle_model(Pro)
    handle_model(Contra)
    handle_model(Moderation)
    handle_model(Preference)
    handle_model(Resistance)


def reverse_last_activity(apps, schema_editor):
    for user in get_user_model().objects.all():
        if hasattr(user, 'config'):
            if not (user.config.is_diverse_mod or user.config.is_female_mod):
                user.config.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('initadmin', '0002_userconfig'),
        ('initproc', '0036_resistance'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfig',
            name='last_activity',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.RunPython(init_last_activity, reverse_code=reverse_last_activity),
    ]