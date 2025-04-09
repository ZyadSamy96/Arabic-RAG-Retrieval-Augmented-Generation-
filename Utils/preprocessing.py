import re 

def normalize_arabic_text(text):
    # Replace instances of merged words (Arabic characters close together)
    # Add spaces after Arabic letters followed by non-Arabic characters or numbers
    text = re.sub(r'([ء-ي])([^\sء-ي])', r'\1 \2', text)
    text = re.sub(r'([^\sء-ي])([ء-ي])', r'\1 \2', text)

    # Normalize common Arabic letters and remove diacritics
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى', 'ي', text)
    text = re.sub(r'ة', 'ه', text)
    
    # Remove Tashkeel (Arabic diacritics)
    text = re.sub(r'[\u064B-\u0652]', '', text)
    
    # Add more space corrections if necessary
    
    return text

def clean_arabic_text(text):
    # Remove repetitive nonsense patterns like "لالالالالالالالالا"
    text = re.sub(r'(.)\1{2,}', ' ', text)  # Remove any character repeated more than 3 times in a row
    
    # Generalize to remove any repeating patterns of 2 or more characters repeated 3 or more times
    text = re.sub(r'(..)\1{2,}', ' ', text)  # Remove two-character patterns repeated 3 or more times (e.g., "لالالالا")
    
    # Keep Arabic characters, numbers, %, $, EGP, €, £, and spaces
    text = re.sub(r'[^\u0600-\u06FF0-9\s%$€£EGP]', ' ', text)  # Keep Arabic characters, numbers, %, $, €, £, EGP, and spaces
    
    # Remove single letters or standalone words of length 1 (e.g., "س" at the end)
    text = re.sub(r'\b\w\b', '', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    
    # text = re.sub(r'(.)\1{2,}', ' ', xxxx)

    # Remove citations or copyright symbols like [1] or ©
    text = re.sub(r'(\[\d+\]|©)', '', text)

    # Remove non-content sections (metadata, references, etc.)
    metadata_keywords = ["تصنيفات:", "آخر تعديل", "سياسة الخصوصية", "مدع", "المعرفات الخارجية"]
    for keyword in metadata_keywords:
        text = re.split(keyword, text)[0]

    return text.strip()
