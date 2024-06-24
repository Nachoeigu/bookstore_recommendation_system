from langchain_core.prompts import ChatPromptTemplate
from constants import SYSTEM_PROMPT
from langchain_core.runnables import RunnableLambda
from langchain_community.callbacks import get_openai_callback
from langchain.output_parsers import PydanticOutputParser
from src.vdb_generator.functions import *
from src.executor.pydantic_classes import *


class BookRecommender:

    def __init__(self, model):
        self.model_with_tool = model.bind_tools([StructuredLLMOutput])
        self.vectorstore = open_vectorstore()
        self.prompt_template = self.__defining_prompt_template()
        self.__developing_chain()

    def __defining_prompt_template(self):
        prompt_template = ChatPromptTemplate.from_messages([
                    ("system", SYSTEM_PROMPT),
                    ("human", "{input_message}")
                    ]
                )

        return prompt_template

    def __searching_in_vdb(self, structured_query):
        print("Searching in the vectorstore...")
        return self.vectorstore.similarity_search(
                    query = structured_query['text'],
                    filter= cleaning_metadata_filters(structured_query)
                )

    def __developing_chain(self):
        self.chain = self.prompt_template \
                        | self.model_with_tool\
                            | RunnableLambda(parse_model_response)


    def answer_query(self, query:str):

        structured_query_for_vectorstore = self.chain.invoke({'input_message': query})
        print(f"The user query was structured: \n {structured_query_for_vectorstore}")
        result = self.__searching_in_vdb(structured_query_for_vectorstore)

        if result == []:
            return "Sorry, we don´t have any book with that specifications"
        else:
            return "We have the following books that you might be interested:\n\n" + '-\n'.join([book.metadata['title'] for book in result]) + "\n Don´t forget to visit our bookstore :)"


