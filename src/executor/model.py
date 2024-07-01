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
        vdb_output = self.vectorstore.similarity_search_with_relevance_scores(
                    query = structured_query['text'],
                    filter= cleaning_metadata_filters(structured_query)
                )
        
        return vdb_output

    def __structuring_vdb_output(self, vdb_output: list) -> str:
        if vdb_output == []:
            return "Sorry, we don´t have any book with that specifications. Try with other question..."
        else:
            return "We have the following books that you might be interested:\n\n" + '-\n'.join([book.metadata['title'] for book in vdb_output]) + "\n Don´t forget to visit our bookstore :)"
        
    def __evaluating_score(self, vdb_output: list) -> str:
        threshold_score = 0.85
        return [document[0] for document in vdb_output if document[1] >= threshold_score]
        
    

    def __developing_chain(self):
        self.chain = self.prompt_template \
                        | self.model_with_tool\
                            | RunnableLambda(parse_model_response) \
                                | RunnableLambda(self.__searching_in_vdb) \
                                    | RunnableLambda(self.__evaluating_score) \
                                        | RunnableLambda(self.__structuring_vdb_output)



    def answer_query(self, query:str):

        return self.chain.invoke({'input_message': query})

