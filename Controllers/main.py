import sys 
sys.path.append('D:\Zyad Codes\zenith')
from fastapi import FastAPI, HTTPException
from Utils.file_utils import download_from_gdrive
from Utils.qdrant_util import QdrantDB
from Utils.pdf_utils import process_pdf
from Definitions.definitions import ProcessPDFRequest,QueryDocumentRequest,FileDownloadRequest
from Configuration.configuration import Service
import uvicorn


app = FastAPI()

        
@app.post("/download")
def download_file(request: FileDownloadRequest):

    try:
        file_path = download_from_gdrive(request.url, request.file_name)
        return {"message": f"File successfully downloaded to {file_path}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/process_pdf")
def process_pdf_endpoint(request: ProcessPDFRequest):

    try:
        qdrant_db = QdrantDB()

        pdf_path = f"assets/{request.file_name}"
        processed_pdf = process_pdf(pdf_path, chunk_size=200, chunk_overlap=50)

        qdrant_db.upload_to_qdrant(processed_pdf, request.collection_name)
        
        return {"message": f"Processed and uploaded PDF {request.file_name} to collection {request.collection_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the PDF: {e}")


@app.post("/query_document")
def query_document(request: QueryDocumentRequest):

    try:
        qdrant_db = QdrantDB()

        results = qdrant_db.query_qdrant(
            collection_name=request.collection_name,
            query_text=request.query_text
        )

        response = {i: [point.score, point.payload['content']] for i, point in enumerate(results)}

        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the document: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host=Service.HOST, port=Service.PORT)