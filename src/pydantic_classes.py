import os
from dotenv import load_dotenv
import sys

load_dotenv()
WORKDIR=os.getenv("WORKDIR")
os.chdir(WORKDIR)
sys.path.append(WORKDIR)

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Literal, List


class StructuredLLMOutput(BaseModel):
    """Structure in JSON format the user input"""
    text: str = Field(..., description = "The text or topic the user asked without the info of the other attributes")
    price: int = Field(..., ge=0, description = "The maximum price the user can afford. If it is not specified, define as 0")
    rating: Literal[0,1,2,3,4,5] = Field(..., description = "The desired rating of the book. If not provided: 0")
    category: List[Literal['Poetry', 'Historical Fiction', 'Fiction', 'Mystery', 'History', 'Young Adult', 'Business', 'Default', 'Sequential Art', 'Music', 'Science Fiction', 'Politics', 'Travel', 'Thriller', 'Food and Drink', 'Romance', 'Childrens', 'Nonfiction', 'Art', 'Spirituality', 'Philosophy', 'New Adult', 'Contemporary', 'Fantasy', 'Add a comment', 'Science', 'Health', 'Horror', 'Self Help', 'Religion', 'Christian', 'Crime', 'Autobiography', 'Christian Fiction', 'Biography', 'Womens Fiction', 'Erotica', 'Cultural', 'Psychology', 'Humor', 'Historical', 'Novels', 'Short Stories', 'Suspense', 'Classics', 'Academic', 'Sports and Games', 'Adult Fiction', 'Parenting', 'Paranormal','']] = Field(..., description = "The categories that could involve the topic. If not clear, retrieve ['']")

