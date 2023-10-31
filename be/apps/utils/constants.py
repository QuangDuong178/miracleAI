import enum


class MessageRole(enum.IntEnum):
    BOT = 1
    HUMAN = 2


class OpenAIModelVersion(enum.Enum):
    GPT_4 = "gpt4"
    GPT_35 = "gpt35"


class CommonKey(enum.Enum):
    SOURCE = "source"
    PAGE = "page"
    DOCUMENT_ID = "document_id"
    METADATA = "metadata"


class ReferTypeEnum(enum.Enum):
    DOCUMENT = '1'
    URL = '2'




class MessageCommon(enum.Enum):
    DOCUMENT = "出典"
    URL = "こちらについては、下記のURLを参照ください"
    NO_ANSWER = "Have no answer for your question"
