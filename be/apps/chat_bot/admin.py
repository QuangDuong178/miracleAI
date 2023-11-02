import threading

from azure.search.documents.indexes.models import SimpleField, SearchFieldDataType, SearchableField, SearchField
from django.conf import settings
from django.contrib import admin
from langchain.document_loaders import PyMuPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import AzureSearch

from apps.chat_bot.models import CustomDataFile, Bot
from apps.utils.constants import CommonKey


def load_documents(file_url, file_name, document_id):
    loader = PyMuPDFLoader(file_url)

    pdf_documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(pdf_documents)
    for document in documents:
        document.metadata[CommonKey.SOURCE.value] = file_name
        document.metadata[CommonKey.DOCUMENT_ID.value] = document_id
        document.metadata[CommonKey.PAGE.value] = int(document.metadata[CommonKey.PAGE.value]) + 1
    return documents


def regenerate_vector(file_url, file_name, document_id):
    embeddings = OpenAIEmbeddings(openai_api_base=settings.OPENAI_API_BASE,
                                  openai_api_version=settings.OPENAI_API_VERSION,
                                  openai_api_key=settings.OPENAI_API_KEY,
                                  openai_api_type=settings.OPENAI_API_TYPE,
                                  deployment=settings.OPENAI_EMBEDDING_DEPLOYMENT_NAME, chunk_size=1,
                                  show_progress_bar=True)
    embedding_function = embeddings.embed_query
    bot = Bot.objects.get(id=1)
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embedding_function("Text")),
            vector_search_configuration=bot.vector_config_name,
        ),
        SearchableField(
            name="metadata",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
    ]
    vector_store = AzureSearch(
        azure_search_endpoint=settings.AZURE_SEARCH_ENDPOINT,
        azure_search_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
        index_name=bot.storage_vector_name,
        fields=fields,
        embedding_function=embeddings.embed_query,
    )

    vector_store.add_documents(load_documents(file_url, file_name, document_id))
    print(f"gen done: {file_name}")

class CustomDataFileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        file_name = obj.file.name
        super().save_model(request, obj, form, change)

        embed_vector_thread = threading.Thread(target=regenerate_vector, name="generate_vector",
                                               args=(obj.file.url, file_name, obj.id), daemon=True)
        embed_vector_thread.start()

class BotAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomDataFile, CustomDataFileAdmin)
admin.site.register(Bot, BotAdmin)

