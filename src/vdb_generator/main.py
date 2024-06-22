import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)
from src.vdb_generator.functions import adding_new_data_to_vectorstore

load_dotenv()


if __name__ == '__main__':
    adding_new_data_to_vectorstore(file_name = f"{WORKDIR}/datasource/data.json")


