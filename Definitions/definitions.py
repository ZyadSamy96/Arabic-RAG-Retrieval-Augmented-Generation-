from pydantic import BaseModel

class FileDownloadRequest(BaseModel):
    url: str
    file_name: str
    
   
class ProcessPDFRequest(BaseModel):
    file_name: str
    collection_name: str
    

class QueryDocumentRequest(BaseModel):
    query_text: str
    collection_name: str