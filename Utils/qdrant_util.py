from qdrant_client import QdrantClient
from Configuration.configuration import QDRANT
from Utils.model import Encoder
from qdrant_client.http import models as qdrant_models
from qdrant_client.http.models import PointStruct, VectorParams

class QdrantDB:
    def __init__(self, url: str = 'http://localhost:6333', api_key: str = '', top_k: int = None, client=None):
        # self.url = QDRANT.URL
        self.url = url
        
        self.api_key = api_key  
        self.top_k = top_k or int(QDRANT.TOP_K)
        
        if client is None:
            self.client = self.create_qdrant_client()
        else:
            self.client = client

    def create_qdrant_client(self):
        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key  
        )
        return self.client

    def get_qdrant_collections(self):
        try:
            return self.client.get_collections()
        except Exception as e:
            print(f"Error getting collections: {str(e)}")
            return None


    def clear_collection(self, collection_name: str):
        if self.client is None:
            self.create_qdrant_client()
        
        try:
            # Check if the collection exists
            self.client.get_collection(collection_name=collection_name)
            
            # Delete the entire collection
            self.client.delete_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' has been deleted.")
            
            # Optionally, recreate the collection if needed
            # You can add logic to recreate the collection with specific settings if needed
        except Exception as e:
            print(f"Error clearing collection: {str(e)}")



    def query_qdrant(self, query_text: str, collection_name: str):
        if self.client is None:
            self.create_qdrant_client()


        query_embedding = Encoder().get_text_embeddings([query_text])[0]
        
        try:
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding.tolist(),
                limit=self.top_k
            )
            return results
        except Exception as e:
            print(f"Error querying Qdrant: {str(e)}")
            return None

    # Adding the upload_to_qdrant function to the class
    def upload_to_qdrant(self, processed_pdf, collection_name):
        encoder = Encoder()
        vector_size = 512  # Assuming CLIP model outputs 512-dimensional vectors

        # Check if collection exists, if not, create it
        try:
            self.client.get_collection(collection_name=collection_name)
        except:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance="Cosine")
            )

        point_id = 0

        # Iterate over the processed PDF data
        for i, entry in enumerate(processed_pdf):
            # Process text chunks first
            text_chunks = entry['chunk']
            print(text_chunks)
            text_embedding = encoder.get_text_embeddings([text_chunks])[0]
            
            # Create a point structure for Qdrant
            point = PointStruct(
                id=point_id,
                vector=text_embedding.tolist(),
                payload={
                    "type": "text", 
                    "content": text_chunks, 
                    "chunk_index": i, 
                    "page": entry['page']
                }
            )
            
            # Upload the text embedding to Qdrant
            self.client.upsert(
                collection_name=collection_name,
                points=[point]
            )
            point_id += 1
        
            # Process images associated with the page
            page_images = entry['images']
            for j, image in enumerate(page_images):
                # Embed the image
                image_embedding = encoder.get_image_embeddings([image])[0]
                
                # Create a point structure for Qdrant
                point = PointStruct(
                    id=point_id,
                    vector=image_embedding.tolist(),
                    payload={
                        "type": "image", 
                        "image_index": j, 
                        "page": entry['page']
                    }
                )
                
                # Upload the image embedding to Qdrant
                self.client.upsert(
                    collection_name=collection_name,
                    points=[point]
                )
                point_id += 1