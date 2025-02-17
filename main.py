import os
import chromadb
import hashlib
import logging
import time
import sys
from chromadb.utils import embedding_functions

logging.basicConfig(level=logging.INFO)

class VectorDB:
    def __init__(self, collection_name="default", use_server=False, host="localhost", port=8000):
        logging.info("Initializing VectorDB")
        if use_server:
            self.client = chromadb.HttpClient(host=host, port=port)
            logging.info(f"Connected to Chroma server at {host}:{port}")
        else:
            self.client = chromadb.Client()
            logging.info("Using Chroma in local mode")
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = embedding_functions.DefaultEmbeddingFunction()

    def insert_document(self, doc_id:str, text:str) -> None:
        """This function will insert the document to Chromadb instance.
        Args:
            doc_id (str): Id of the document for indexing.
            text (str): Text to be inserted
        Returns: None
        """
        logging.info(f"Inserting document ID {doc_id}")
        vector = self.get_embedding(text)
        try:
            self.collection.add(ids=[doc_id], embeddings=[vector], metadatas=[{"text": text}])
            logging.info("Document inserted successfully")
        except Exception as e:
            logging.error(f"Error inserting document: {e}")
            traceback.print_exc()

    def get_embedding(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        return self.embedder([text])[0]

    def update_document(self, doc_id:str, new_text:str) -> None:
        """This function will update the already existing document in Chromadb.
        Args:
            doc_id (str): Document Id to be updated.
            new_text (str): New text to replace the original or existing text in chromadb.
        Returns: None
        """
        logging.info(f"Updating document ID {doc_id}")
        self.delete_document(doc_id)
        self.insert_document(doc_id, new_text)
    
    def create_collection(self, collection_name:str='default') -> None:
        """This function is going to create a collection in the chromadb
        Args:
            collection_name (str, optional): Name of the collection. Defaults to 'default'.
        Returns: None
        """
        logging.info(f"Creating collection: {collection_name}")
        self.collection = self.client.get_or_create_collection(collection_name)

    def delete_document(self, doc_id:str) -> None:
        """This function will delete any already existing document in chromadb.
        Args:
            doc_id (str): Id of the document to be deleted.
        Returns: None
        """
        logging.info(f"Deleting document ID {doc_id}")
        self.collection.delete(ids=[doc_id])
        logging.info("Document deleted successfully")

    def retrieve_documents(self, query_text:str, top_n:int=5) -> list:
        """This function will retrieve the required document based on search string.
        Args:
            query_text (str): Text to be searched in the chromadb.
            top_n (int, optional): Number of nearest matching results to be fetched. Defaults to 5.
        Returns:
            list: list of matching results or empty list in case of no result found.
        """
        logging.info(f"Retrieving top {top_n} documents for query: {query_text}")
        query_vector = self.get_embedding(query_text)
        try:
            results = self.collection.query(query_embeddings=[query_vector], n_results=top_n)
            logging.info(f"Raw results: {results}")
            if results and 'metadatas' in results and results['metadatas']:
                return [meta['text'] for meta in results['metadatas'][0]]
            else:
                logging.warning("No documents returned, only metadata found")
                return []
        except Exception as e:
            logging.error(f"Error during retrieve_documents: {e}")
            traceback.print_exc()
            return []

    def read_text_file(self, filename:str) -> [str]:
        """This function will read the text file.
        Args:
            filename (str): path or name(in case of same directory) of the file.
        Returns:
            [str]: list of lines read from text file.
        """
        if os.path.exists(filename) and filename.endswith(".txt"):
            with open(filename,'r') as fr:
                return fr.readlines()


if __name__ == "__main__":
    db = VectorDB(use_server=True, host="localhost", port=8000)
    db.create_collection()
    data_path = r'sample.txt'
    data = db.read_text_file(data_path)
    db.insert_document('1',"".join(data))
    db.update_document(doc_id='1', new_text="this document is about vector mapping and this is the main document.")
    result = db.retrieve_documents("vector")
    print(f"-->result {result[0]}")
    db.delete_document(doc_id='1')
    result = db.retrieve_documents("vector")