from django.core.validators import FileExtensionValidator, URLValidator
from django.db import models
import environ
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.core.db.models import TimeStampMixin
env = environ.Env()

class Bot(TimeStampMixin):
    storage_vector_name = models.CharField(max_length=128)
    vector_config_name = models.CharField(max_length=128)
    prompt_message = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "bot"

def pdf_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pdf/filename
    return 'pdf/{0}'.format(filename)

class CustomDataFile(TimeStampMixin):
    file = models.FileField(upload_to=pdf_directory_path,
                            validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    class Meta:
        db_table = 'custom_data_file'

