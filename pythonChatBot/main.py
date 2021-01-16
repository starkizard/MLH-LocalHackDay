
from chatbot import Chat, register_call
import wikipedia as wiki
import os
import warnings
warnings.filterwarnings("ignore")


@register_call("whoIs")
def who_is(session, query):
    try:
        return wiki.summary(query)
    except Exception:
        for new_query in wiki.search(query):
            try:
                return wiki.summary(new_query)
            except Exception:
                pass
    return "I dunno "+query


first_question = "How's it going bros , it's your boi pewdieeshit!      "
chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.template"))
chat.converse(first_question)