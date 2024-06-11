from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import JSONLoader


def extract_metadata(record: dict, metadata: dict) -> dict:

    metadata["price"] = record['price in pounds']
    metadata["title"] = record['title']
    metadata["rating"] = record['rating']
    metadata['availability'] = record['availability']
    metadata['category'] = record['category']
    metadata['number of reviews'] = record['number of reviews']
    print("Metadata extracted!")
    return metadata

def transforming_data(file_name):
    loader = JSONLoader(
        file_path=f'{file_name}',
        jq_schema='.[]',
        content_key="description",
        metadata_func=extract_metadata
    )

    data = loader.load()
    print("Loaded data!")
    return data

def pushing_data_to_vectorstore(data):
    PineconeVectorStore.from_documents(
        documents = data,
        index_name='bookstorerecommendation',
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002")
    )
    print("Pushed to Pinecone!")

def adding_new_data_to_vectorstore(file_name):
    data = transforming_data(file_name)
    pushing_data_to_vectorstore(data)

def open_vectorstore():
    vectorstore = PineconeVectorStore(index_name='bookstorerecommendation', embedding=OpenAIEmbeddings(model="text-embedding-ada-002"))
    print("Log in the vectorstore!")

    return vectorstore

def parse_model_response(response):
    return response.tool_calls[0]['args']

def cleaning_metadata_filters(filters):
    output = {}
    for key in filters.keys():
        if key == 'text':
            continue
        elif filters[key] == 0:
            continue
        elif key == 'price':
            output[key] = {'$lte': filters[key]}
        elif key == 'category':
            output[key] = {'$in': filters[key]}
        elif key == 'rating':
            output[key] = {'$gte': filters[key]}
        
        
        else:
            output[key] = filters[key]
    
    return output
