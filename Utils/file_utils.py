import gdown

def download_from_gdrive(url, file_name):

    try:
        # Extract file ID from the URL
        file_id = url.split('/')[-2]
        download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        # Download the file
        gdown.download(download_url, f"assets/{file_name}", quiet=False)
        print(f"File successfully downloaded to {file_name}")
    except Exception as e:
        print(f"Error downloading the file: {e}")

# if __name__ == "__main__":
#     download_from_gdrive('https://drive.google.com/file/d/1kwfqgv54aFUFGaEz8xSn_GDVyQZqYepG/view?usp=drive_link', '2.pdf')
