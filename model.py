from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import io
import requests
from bs4 import BeautifulSoup
from db import DB


class Model:

    def __init__(self) -> None:
        self.converse = None
        self.db = DB()

    @staticmethod
    async def get_raw_txt(pdf_docs):
        print("processing pdfs...")
        text = ""
        for pdf in pdf_docs:
            contents = await pdf.read()
            pdf_file = io.BytesIO(contents)
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        print(text)
        return text

    @staticmethod
    def get_txt_chunks(text):
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks

    @staticmethod
    def get_vectors(text_chunks):
        embeddings = OpenAIEmbeddings()
        vectors = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vectors

    @staticmethod
    def get_conv_chain(vectorstore):
        llm = ChatOpenAI()
        # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory
        )
        return conversation_chain

    @staticmethod
    def web_scrap_to_txt(url):
        print("started webscraping...")
        content = []
        response = requests.get(url)

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract specific elements from the HTML
        title = soup.title.text
        paragraphs = soup.find_all('p')
        content.append(title)

        print("completed capturing title")
        for p in paragraphs:
            content.append(p.text)
        return ' '.join(content)

    async def model_data(self, pdf_docs="", url=""):
        raw_text = ""

        if pdf_docs is not None:
            raw_text = await self.get_raw_txt(pdf_docs)
        if url is not None:
            raw_text += self.web_scrap_to_txt(url)
        print("completed processing")
        db_data = self.db.get_data()
        print("completed getting data")
        db_data = db_data + " ".join(self.get_txt_chunks(raw_text))
        vectordb = self.get_vectors([db_data])
        print("completed vectorization")
        self.converse = self.get_conv_chain(vectordb)
        self.db.store_data(db_data)
        print("completed model creation")
        return self.converse

    def get_model(self):
        return self.converse
