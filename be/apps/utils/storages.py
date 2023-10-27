from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    """ImageField & FileField push to Azure blob storage"""
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.MEDIA_LOCATION
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = settings.STATIC_LOCATION
    expiration_secs = None
