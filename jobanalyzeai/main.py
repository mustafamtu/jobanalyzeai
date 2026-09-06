from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory



load_dotenv()

with open("ilan.txt","r",encoding="utf-8") as ilan:
    ilan_metni = ilan.read()


if ilan_metni.strip() == (""):
    raise Exception("İlan Metni Bulunamadı.")

with open("cv.txt","r",encoding="utf-8") as cv:
    cv_metni = cv.read()

if cv_metni.strip() == (""):
    raise Exception("CV Metni Bulunamadı.")

LLM = GoogleGenerativeAI(model="gemini-2.5-flash")

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///history.db",
    )

metin = f"""
    Sen bir kariyer uzmanısın işin sana gelen ilan metnini detaylıca okumak 
    kullanıcının özgeçmişi, yetenekleriyle kıyaslamak ve ilanın kullanıcıya 
    göre eksi ve artı yanlarını analiz et çok kısa olsun bu yönler üç tane artı 
    üç tane eksi yön belirle ve bunları üç tane bir cümlelik metinlerle ver
    son olarak bir puan belirle 100 üzerinden (100 çok uyumlu ilan, 0 hiç uyum olmayan ilan)


    örnek:

        'Artı Yönler:' +'artı örnek 1'
                       +'artı örnek 2'
                       +'artı örnek 3'

        'Eksi Yönler:' -'eksi örnek 1'
                       -'eksi örnek 2'
                       -'eksi örnek 3'

        'Puan': '?'
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", metin),
    ("human", "İlan \n{ilan},\n {cv}")
])

chain = prompt | LLM

cevap = chain.invoke(
    {"ilan": ilan_metni, "cv": cv_metni}
)
print(cevap)
