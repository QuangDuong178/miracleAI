from django.core.validators import FileExtensionValidator, URLValidator
from django.db import models
import environ
from apps.core.db.models import TimeStampMixin
env = environ.Env()

def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/master_<filename>
    return 'avatar/master_{0}'.format(filename)

class Bot(TimeStampMixin):
    storage_vector_name = models.CharField(max_length=128)
    vector_config_name = models.CharField(max_length=128)
    prompt_message = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "bot"

def pdf_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pdf/<master vector name>/filename
    return 'pdf/{0}/{1}'.format(instance.bot.storage_vector_name, filename)

class CustomDataFile(TimeStampMixin):

    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    file = models.FileField(upload_to=pdf_directory_path,
                            validators=[FileExtensionValidator(allowed_extensions=["pdf"])])

    class Meta:
        db_table = 'custom_data_file'