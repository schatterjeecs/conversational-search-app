from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import asyncio

from fastapi import Depends, HTTPException

from model import Model
from dotenv import load_dotenv
import os
from typing import List, Annotated

app = FastAPI()
model_obj = Model()
chat_history = []

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

ALLOWED_PDF_EXTENSIONS = [".pdf"]


def allowed_file(filename: str) -> bool:
    ext = os.path.splitext(filename)[1]
    return ext.lower() in ALLOWED_PDF_EXTENSIONS


class Search(BaseModel):
    query: str


@app.get("/healthcheck")
async def root():
    return {"message": "Status: OK"}


@app.post("/genmodel")
async def gen_model(pdf_docs: Annotated[List[UploadFile], File()] = None,
                    url: Annotated[str, Form()] = None,
                    ):
    if pdf_docs is None and url is None:
        raise HTTPException(status_code=500, detail="Atleast one param of `pdf_docs` and `url` required.")

    print("uploaded")
    if pdf_docs is not None:
        for file in pdf_docs:
            if not allowed_file(file.filename):
                raise HTTPException(status_code=400, detail="Invalid file extension")
    await model_obj.model_data(pdf_docs=pdf_docs, url=url)
    return {"message": "Model Generated"}


@app.get("/search")
async def search(query_data: Search):
    query = query_data.query
    print(f"query: {query}")
    converse = model_obj.get_model()
    if converse is None:
        raise HTTPException(status_code=500, detail="Model Not Generated")
    response = converse({"question": query})
    chat_history.append(response['chat_history'])
    return response['answer']