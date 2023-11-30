import os
import hashlib
from datetime import datetime
from transformers import pipeline

LABELS = ['urgent', 'not urgent']


def get_folder_meta_data(folder_path):
    try:
        # List all items (files and folders) in the given folder
        items = [item for item in os.listdir(folder_path)]

        # Separate files and folders
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
        folders = [item for item in items if os.path.isdir(os.path.join(folder_path, item))]

        # Count the number of files and folders
        num_files = len(files)
        num_folders = len(folders)

        size = os.path.getsize(folder_path)
        last_access_time = os.path.getatime(folder_path)
        last_modification_time = os.path.getmtime(folder_path)
        
        access_time = datetime.fromtimestamp(last_access_time).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.fromtimestamp(last_modification_time).strftime('%Y-%m-%d %H:%M:%S')

        meta_data = {
            'size': size,
            'last_access_time': access_time,
            'last_modification_time': modification_time,
            'number of files': num_files,
            'number of folders': num_folders
        }

        return meta_data
    
    except OSError as e:
        # Handle exceptions, if the folder doesn't exist
        print(f"Error: {e}")
        return None


def hash_file(file_path):
    with open(file_path, "rb") as f:
        h = hashlib.new('sha256')
        # Read the file in chunks to handle large files
        chunk_size = 8192
        for chunk in iter(lambda: f.read(chunk_size), b''):
            h.update(chunk)

    return h.hexdigest()


def classify_document(document):
    with open(document.file_path, "r") as f:
        # Perform document classification using zero-shot-classification generative AI model
        pipe = pipeline('zero-shot-classification')
        classification_result = pipe(str(f.read()), candidate_labels=LABELS)

        # Update the classification label in the database
        document.classification_label = classification_result['labels'][0]
        document.save()