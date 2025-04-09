from Utils.qdrant_util import QdrantDB
from Utils.pdf_utils import process_pdf

if __name__ == "__main__":

# Define the path to the PDF file
    pdf_path = "assets/renewable_energy_arabic_wikipedia.pdf"

    qdrant_db = QdrantDB()

    # Example PDF processing (you should have a function that processes your PDFs)
    processed_pdf = process_pdf(pdf_path, chunk_size=200, chunk_overlap=50)

    # Upload the processed data to Qdrant
    qdrant_db.upload_to_qdrant(processed_pdf, "my_qdrant_collection2")
