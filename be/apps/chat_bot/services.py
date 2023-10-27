import json
import logging
import queue
from itertools import groupby

from django.conf import settings
from langchain import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import AzureCognitiveSearchRetriever

from apps.chat_bot.models import ReferUrl, CustomDataFile
from apps.utils.constants import MessageRole, CommonKey, ReferTypeEnum, DisplayReferType, MessageCommon


# conversation
class ThreadedGenerator:
    def __init__(self):
        self.queue = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        item = self.queue.get()
        if item is StopIteration:
            raise item
        return item

    def send(self, data):
        self.queue.put(data)

    def close(self):
        self.queue.put(StopIteration)


class ChainStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, gen):
        super().__init__()
        self.gen = gen

    def on_llm_new_token(self, token: str, **kwargs):
        self.gen.send(token)


class SimpleConversationChat:
    def __init__(self, history):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
        self.set_memory(history)

    def set_memory(self, history):
        for message in history:
            if message.get("role") == MessageRole.BOT.value:
                self.memory.chat_memory.add_ai_message(message.get("message"))
            elif message.get("role") == MessageRole.HUMAN.value:
                self.memory.chat_memory.add_user_message(message.get("message"))

    def generator(self, master, user_message):
        # g = ThreadedGenerator()
        # threading.Thread(target=self.llm_thread, args=(g, master, user_message)).start()
        return self.llm_thread(master, user_message)

    def llm_thread(self, master, user_message):
        final_message = []
        try:

            condense_template = """
                次の会話とフォローアップの質問を考慮し、フォローアップの質問を独立した質問として言い換えます。
    
                チャット履歴:
                {chat_history}
                フォローアップ入力：{question}
                独立した質問:
                """

            condense_question_prompt = PromptTemplate(
                template=condense_template,
                input_variables=["chat_history", "question"]
            )

            qa_prompt_message = master.prompt_message if master.prompt_message \
                else "最後の質問に丁寧な日本語で答えるには、次の文脈を使用します。 文脈内のデータがない場合、または答えがわからない場合は、答えを考え出そうとせず、ただわからないと言ってください。"

            qa_template = qa_prompt_message + """答えがわからない質問については、答えの最後に「NO」を追加する必要があります。
            {context}
            {chat_history}

            質問：{question}
            回答：
            """

            qa_prompt = PromptTemplate(
                template=qa_template,
                input_variables=["context", "question", "chat_history"]
            )

            retriever = AzureCognitiveSearchRetriever(content_key="content", index_name=master.storage_vector_name,
                                                      api_key=settings.AZURE_COGNITIVE_SEARCH_API_KEY,
                                                      service_name=settings.AZURE_COGNITIVE_SEARCH_SERVICE_NAME,
                                                      top_k=5)

            llm = AzureChatOpenAI(
                openai_api_base=settings.OPENAI_API_BASE,
                openai_api_version=settings.OPENAI_API_VERSION,
                deployment_name=settings.OPENAI_CONVERSATION_DEPLOYMENT_NAME,
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_type=settings.OPENAI_API_TYPE,
                temperature=0.2,
                request_timeout=120,
                # streaming=True,
                # callback_manager=CallbackManager([ChainStreamHandler(g)]),
            )
            conv = ConversationalRetrievalChain.from_llm(
                llm=llm,
                memory=self.memory,
                retriever=retriever,
                return_source_documents=True,
                condense_question_prompt=condense_question_prompt,
                combine_docs_chain_kwargs={"prompt": qa_prompt}
            )
            bot = conv({"question": user_message})

            source_documents = []
            for document in bot.get("source_documents"):
                if document.metadata.get(CommonKey.METADATA.value):
                    metadata = (json.loads(document.metadata.get(CommonKey.METADATA.value)))
                    document_id = metadata.get(CommonKey.DOCUMENT_ID.value) if metadata.get(
                        CommonKey.DOCUMENT_ID.value) else None
                    if master.refer_type == ReferTypeEnum.DOCUMENT.value:
                        data_file = CustomDataFile.objects.get(id=document_id)

                        if data_file.display_refer_type == DisplayReferType.NO_DISPLAY.value:
                            continue

                        source_documents.append({
                            CommonKey.SOURCE.value: metadata.get(CommonKey.SOURCE.value),
                            "page": metadata.get(CommonKey.PAGE.value) if (metadata.get(
                                CommonKey.PAGE.value) is not None and data_file.display_refer_type == DisplayReferType.FILE_WITH_PAGE.value) else None
                        })
                    elif master.refer_type == ReferTypeEnum.URL.value:
                        refer_urls = ReferUrl.objects.filter(file_id=document_id).values_list("url", flat=True)
                        source_documents.extend(refer_urls)

            source_info = ''
            bot_answer = bot.get("answer")

            if not source_documents:
                final_message.append(MessageCommon.NO_ANSWER.value)
            elif master.refer_type == ReferTypeEnum.DOCUMENT.value:

                source_documents.sort(key=lambda doc: doc.get(CommonKey.SOURCE.value))
                source_documents = [
                    {filename: [
                        str(data.get(CommonKey.PAGE.value)) if data.get(CommonKey.PAGE.value) is not None else None for
                        data
                        in document]} for
                    filename, document in
                    groupby(source_documents, key=lambda x: x.get(CommonKey.SOURCE.value))]

                for document in source_documents:
                    for filename, list_page in document.items():
                        list_page = list(filter(lambda page: page is not None, list_page))
                        if not list_page:
                            source_info += "\n" + filename
                        else:
                            source_info += "\n" + f" {filename} - ページ番号: {', '.join(set(list_page))}"

                if "NO" not in bot_answer and source_info:
                    final_message.append(f"{bot_answer}\n")
                    final_message.append(f"{MessageCommon.DOCUMENT.value}: {source_info}")

                else:
                    final_message.append(MessageCommon.NO_ANSWER.value)
            elif master.refer_type == ReferTypeEnum.URL.value and source_documents:
                source_documents = map(convert_to_link, set(source_documents))
                source_info = "\n" + "\n".join(set(source_documents))

                if "NO" not in bot_answer and source_info:
                    final_message.append(f"{MessageCommon.DOCUMENT.value}: {source_info}")
                else:
                    final_message.append(MessageCommon.NO_ANSWER.value)

            logging.info(f"Answer message: {bot.get('answer')}")
            logging.info(f"Conversation History: {bot.get('chat_history')}")

        except Exception as e:
            logging.error(f"Can't return answer with error {e}")
            final_message.append(MessageCommon.NO_ANSWER.value)

        finally:
            return "".join(final_message)


def convert_to_link(item):
    link_element = f"<a href='{item}' target='_blank'>{item}</a>"
    return link_element


def streaming_response(master, history_messages):
    history = history_messages[:-1]
    human_message = history_messages[-1]

    chat = SimpleConversationChat(history)
    ai_message = ""
    for chunk in chat.generator(master=master, user_message=human_message.get("message")):
        ai_message += chunk
        yield chunk
