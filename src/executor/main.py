import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from src.executor.model import BookRecommender

load_dotenv()

if __name__ == '__main__':
    model = ChatOpenAI(model="gpt-3.5-turbo", temperature = 0)
    #model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature = 0)
    while True:

        query = input("What do you want to read?\n")
        bot = BookRecommender(model = model)
        print(bot.answer_query(query = query))
        print("-------------------")

