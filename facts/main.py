from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from dotenv import load_dotenv
import langchain


langchain.debug = True
# โหลดค่า environment จากไฟล์ .env 
load_dotenv()

embeddings = OpenAIEmbeddings()


# แยกข้อความจากเอกสารเป็นชิ้นเพื่อให้ง่ายต่การค้นหาและเข้าถึงด้วยการเปรียบเทียบในรูปการของการให้ค่าความถี่ของคำที่้หมือนกันหรือใกล้เคียงกันในรูปแบบความเป็นบวกและลบของความหมายของคำด้วยกระบวนการที่มีชื่อว่า embeddings
# เราจะแยกข้อความด้วยอะไรในที่นี่จะแยกด้วยการขึ้นบันทัดใหม่ก้คือใช่ sepator="\n"
# จำนวนของตัวอักษรที่ต้องการตัดวนแต่ละก้อนข้อความ chunk_size={number} 
# หากต้องให้ต้องการให้มีการซ้ำของข้อมูลบางส่วนของแตละก้อนข้อความให้กำหนด chunk_overlap={number}
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=200,
    chunk_overlap=0
)

# โหลดไฟล์ที่ต้องการใช้เข้ามาในระบบ
loader = TextLoader("facts.txt")

# ให้แยกข้อความจากไฟล์เป็นชิ้นตามที่เรากำหนดในฟังชั่น CharacterTextSplitter() ด้านบน
docs = loader.load_and_split(
    text_splitter=text_splitter
)

# To store embeddings data on Chromadb weneed to install ChromaDB with command$ pip install chromadb
db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="emb"
)

results = db.similarity_search(
    # คำถาม
    "what is interresting about the english language?",

    # จำนวนของผลลัพธ์ที่ต้องการให้แสดง
    k=4
    )

for result in results:
    print("\n")
    ## เพื่อดู score ของชุดข้อมูลที่ทำการแบ่งจากด้านบน CharacterTextSplitter
    # print(result[1]) 

    # เพื่อดูข้อมูลที่ทำการค้นหาเสร็จแล้ว
    print(result.page_content)