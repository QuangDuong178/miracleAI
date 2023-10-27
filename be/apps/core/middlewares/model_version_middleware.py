import json

import environ
from django.conf import settings

from apps.utils.constants import OpenAIModelVersion


class ModelVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        env = environ.Env()

        version_get_request = request.GET.get("version")

        version_post_request = None
        if request.method == "POST":
            try:
                version_post_request = (json.loads(request.body)).get("model")
            except Exception:
                pass

        if version_get_request == OpenAIModelVersion.GPT_4.value or version_post_request == OpenAIModelVersion.GPT_4.value:
            settings.OPENAI_API_BASE = env("OPENAI_API_BASE_V2")
            settings.OPENAI_API_KEY = env("OPENAI_API_KEY_V2")
            settings.OPENAI_CONVERSATION_DEPLOYMENT_NAME = env("OPENAI_CONVERSATION_DEPLOYMENT_NAME_V2")
            settings.OPENAI_EMBEDDING_DEPLOYMENT_NAME = env("OPENAI_EMBEDDING_DEPLOYMENT_NAME_V2")

        response = self.get_response(request)

        return response
