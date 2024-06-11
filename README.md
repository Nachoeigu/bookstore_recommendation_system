# Bookstore Recommendation System

## What about this?

Based on Large Language Models and Vector Databases as core, this is a software that suggests to you books from the bookstore "BooksToScrape".

## How it works?

Tell to the bot what are your interests and the bot will retrieve to you the most interesting books for your preferences.
### Under the hood?
Basicaly, I populated a Vector Database, on Pinecone, with the embeddings that represent each book. With that VDB as data source, I utilized a LLM to structure the unustructed input from the user in a way that then I can filter efficiently over the records based on the metadata and the cosine similarity search implemented.
