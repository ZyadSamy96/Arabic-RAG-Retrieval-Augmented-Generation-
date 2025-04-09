from pdf2image import convert_from_path
import pytesseract
from Utils.images import extract_image_boxes
import re
from Utils.preprocessing import clean_arabic_text, normalize_arabic_text

def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return images

def split_into_sentences(text):
    # Split text into sentences using punctuation marks (., ؟, !)
    sentence_endings = r'[.!؟]+'
    sentences = re.split(sentence_endings, text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def split_into_paragraphs(text):
    # Split the text by double newlines or single newlines to capture paragraphs
    paragraphs = text.split('\n\n')  # Split by two newlines to handle paragraph boundaries
    return [p.strip() for p in paragraphs if p.strip()]  # Remove empty paragraphs

def strict_split(text, chunk_size, chunk_overlap):
    # Split long text into smaller chunks with overlap
    final_chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        final_chunks.append(text[start:end])
        # Move the start by chunk_size minus the overlap
        start = end - chunk_overlap
    return final_chunks

def split_page_content(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    
    # Step 1: Clean the text from noisy characters
    clean_content = clean_arabic_text(normalize_arabic_text(text))
    
    # Step 2: Split text into paragraphs
    paragraphs = split_into_paragraphs(clean_content)
    
    # Step 3: For each paragraph, split into sentences
    for paragraph in paragraphs:
        sentences = split_into_sentences(paragraph)
        full_text = '. '.join(sentences)
        
        # Ensure no chunk exceeds the size limit
        if len(full_text) > chunk_size:
            smaller_chunks = strict_split(full_text, chunk_size, chunk_overlap)
            chunks.extend(smaller_chunks)
        else:
            chunks.append(full_text)

    return chunks

def process_pdf(pdf_path, chunk_size=500, chunk_overlap=50):
    # Convert PDF pages to images
    pages = convert_from_path(pdf_path)
    
    processed_pdf = []
    
    # Process each page
    for page_num, page in enumerate(pages):
        print(f"Processing page {page_num + 1}...")
        
        # Extract Arabic text from the page using Tesseract
        text = pytesseract.image_to_string(page, lang='ara')
        
        # Split the page content into chunks
        page_chunks = split_page_content(text, chunk_size, chunk_overlap)
        page_images = extract_image_boxes(page)
        
        # Store the chunks with the corresponding page number and images
        for chunk in page_chunks:
            processed_pdf.append({
                'page': page_num + 1,
                'chunk': chunk,
                'images': page_images,
            })
    
    return processed_pdf