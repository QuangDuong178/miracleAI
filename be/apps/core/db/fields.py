from django.conf import settings
from django.db import models


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == settings.DATABASE_ENGINE:
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == settings.DATABASE_ENGINE:
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)
