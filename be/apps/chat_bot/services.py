import json
import logging
import queue

from django.conf import settings
from langchain import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import AzureCognitiveSearchRetriever

from apps.utils.constants import MessageRole, CommonKey, MessageCommon


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

    def generator(self, bot, user_message):
        # g = ThreadedGenerator()
        # threading.Thread(target=self.llm_thread, args=(g, master, user_message)).start()
        return self.llm_thread(bot, user_message)

    def llm_thread(self, bot, user_message):
        try:

            condense_template = """
                Consider the following conversation and follow-up questions, and rephrase the follow-up questions as stand-alone questions.
    
                Chat history:
                {chat_history}
                Follow-up input：{question}
                Independent question:
                """

            condense_question_prompt = PromptTemplate(
                template=condense_template,
                input_variables=["chat_history", "question"]
            )

            qa_prompt_message = bot.prompt_message if bot.prompt_message \
                else "To answer the last question in polite Vietnamese, use the following context: If you don't have data in context or don't know the answer, don't try to come up with an answer, just say you don't know."

            qa_template = qa_prompt_message + """
            {context}
            {chat_history}

            Question：{question}
            Answer：
            """

            qa_prompt = PromptTemplate(
                template=qa_template,
                input_variables=["context", "question", "chat_history"]
            )

            retriever = AzureCognitiveSearchRetriever(content_key="content", index_name=bot.storage_vector_name,
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

            return bot.get("answer")

        except Exception as e:
            logging.error(f"Can't return answer with error {e}")
            return MessageCommon.NO_ANSWER.value


def convert_to_link(item):
    link_element = f"<a href='{item}' target='_blank'>{item}</a>"
    return link_element


def streaming_response(bot, history_messages):
    history = history_messages[:-1]
    human_message = history_messages[-1]

    chat = SimpleConversationChat(history)
    ai_message = ""
    for chunk in chat.generator(bot=bot, user_message=human_message.get("message")):
        ai_message += chunk
        yield chunk
