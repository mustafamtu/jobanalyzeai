from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
import sqlite3

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



metin = f"""
    Sen bir kariyer uzmanısın işin sana gelen ilan metnini detaylıca okumak 
    kullanıcının özgeçmişi, yetenekleriyle kıyaslamak ve ilanın kullanıcıya 
    göre eksi ve artı yanlarını analiz et çok kısa olsun bu yönler üç tane artı 
    üç tane eksi yön belirle ve bunları üç tane bir cümlelik metinlerle ver
    son olarak bir puan belirle 100 üzerinden (100 çok uyumlu ilan, 0 hiç uyum olmayan ilan)


    örnek:

    Şirket Adı: "Örnek Şirket"
    Pozisyon: "Örnek Pozisyon"

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
    ("human", "İlan \n{ilan},\n {cv},\n {format_instructions}")
])

db_file_path = "gecmis.db"

conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()
cursor.execute(
"""
CREATE TABLE IF NOT EXISTS analizler(
id INTEGER PRIMARY KEY AUTOINCREMENT,
sirket TEXT,
pozisyon TEXT,
artiyonler TEXT,
eksiyonler TEXT,
puan INTEGER,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
)
conn.commit()


class Analiz(BaseModel):
    sirket: str = Field(description="İlanı yayımlayan şirketin adı")
    pozisyon: str = Field(description="İlandaki pozisyon")
    artiyonler: list[str] = Field(description="Adayın artı yönleri (3 madde)")
    eksiyonler: list[str] = Field(description="Adayın eksi yönleri (3 madde)")
    puan: int = Field(description="İlan uyumluluk puanı")

parser = JsonOutputParser(pydantic_object=Analiz)

format_instructions= parser.get_format_instructions()

chain = prompt | LLM | parser

cevap = chain.invoke(
    {"ilan": ilan_metni, "cv": cv_metni, "format_instructions": format_instructions}
)
print(cevap)

sirket_adi = cevap["sirket"]
pozisyon_tanimi = cevap["pozisyon"]
artilar_metin = "\n".join(cevap["artiyonler"])
eksiler_metin = "\n".join(cevap["eksiyonler"])
puan_degeri = cevap["puan"]

cursor.execute(
    """
    INSERT INTO analizler (sirket,pozisyon,artiyonler, eksiyonler, puan) VALUES (?,?,?,?,?)
    """,
    (sirket_adi,pozisyon_tanimi,artilar_metin,eksiler_metin,puan_degeri)
)
conn.commit()
conn.close()
