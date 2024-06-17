import os
from dotenv import load_dotenv
import sys
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from src.model import BookRecommender

app = FastAPI()
model = ChatOpenAI(model="gpt-3.5-turbo", temperature = 0)
#model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature = 0)

bot = BookRecommender(model = model)

@app.get('/')
def main():
    return {'Starting': "App running..."}

@app.get("/query_books")
def get_books(preferences: str) -> str:
    return bot.answer_query(query = preferences)

#uvicorn app:app --host 0.0.0.0 --port 80