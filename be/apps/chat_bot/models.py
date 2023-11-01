from django.core.validators import FileExtensionValidator, URLValidator
from django.db import models

from apps.core.db.models import TimeStampMixin


def avatar_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/avatar/master_<filename>
    return 'avatar/master_{0}'.format(filename)


REFER_TYPE_CHOICES = (
    ('1', "Document Sources"),
    ('2', "URL")
)


class MasterConversation(TimeStampMixin):
    name = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    storage_vector_name = models.CharField(max_length=128)
    vector_config_name = models.CharField(max_length=128)
    avatar = models.ImageField(null=True, blank=True)
    prompt_message = models.TextField(max_length=1000, null=True, blank=True)
    refer_type = models.CharField(choices=REFER_TYPE_CHOICES, max_length=128, default=1)

    class Meta:
        db_table = "master_conversation"

    def __str__(self):
        return self.name


def pdf_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pdf/<master vector name>/filename
    return 'pdf/{0}/{1}'.format(instance.master.storage_vector_name, filename)


DISPLAY_REFER_CHOICES = (
    ("1", "File + Page"),
    ("2", "File Only"),
    ("3", "No Display"),
)


class CustomDataFile(TimeStampMixin):
    master = models.ForeignKey(MasterConversation, on_delete=models.CASCADE)
    description = models.CharField(max_length=128, blank=True, null=True)
    file = models.FileField(upload_to=pdf_directory_path,
                            validators=[FileExtensionValidator(allowed_extensions=["pdf","csv"])])
    display_refer_type = models.CharField(max_length=20, choices=DISPLAY_REFER_CHOICES, default=1)

    class Meta:
        db_table = 'custom_data_file'

    def __str__(self):
        return f"{self.master.name}__{self.file.name}"


class ReferUrl(TimeStampMixin):
    file = models.ForeignKey(CustomDataFile, on_delete=models.CASCADE)
    url = models.CharField(max_length=128, blank=False, null=True, validators=[URLValidator()])

    class Meta:
        db_table = 'refer_url'
