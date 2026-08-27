from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

LLM = GoogleGenerativeAI(model="gemini-2.5-flash")

with open("ilan.txt","r",encoding="utf-8") as ilan:
    ilan_metni = ilan.read()
    ilan.close()

with open("cv.txt","r",encoding="utf-8") as cv:
    cv_metni = cv.read()
    cv.close()

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
