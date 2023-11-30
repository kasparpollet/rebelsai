import os
import hashlib
import textract
import nltk
from nltk.corpus import stopwords
from datetime import datetime
from transformers import pipeline

from core.models import Document

LABELS = ['urgent', 'not urgent']


def build_tree(folder_path: str) -> dict:
    tree = {'name': os.path.basename(folder_path), 'type': 'dir', 'children': []}

    try:
        # List all items (files and folders) in the given folder
        items = os.listdir(folder_path)

        for item in items:
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                # Recursively build tree for subdirectories
                subtree = build_tree(item_path)
                tree['children'].append(subtree)
            else:
                tree['children'].append({'name': item, 'type': 'file'})

    except OSError as e:
        print(f"Error: {e}")

    return tree


def count_sub_folders_and_files(folder_path: str) -> dict:
    try:
        num_files = 0
        num_folders = 0

        items = [item for item in os.listdir(folder_path)]

        for item in items:
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                num_files += 1
            elif os.path.isdir(item_path):
                subfolder_stats = count_sub_folders_and_files(item_path)
                num_files += subfolder_stats['num_files']
                num_folders += subfolder_stats['num_folders'] + 1

        return {
            'num_files': num_files,
            'num_folders': num_folders
        }
    
    except OSError as e:
        print(f"Error: {e}")
        return {'num_files': 0, 'num_folders': 0}


def get_folder_meta_data(folder_path: str) -> dict:
    try:
        count = count_sub_folders_and_files(folder_path)

        size = os.path.getsize(folder_path)
        last_access_time = os.path.getatime(folder_path)
        last_modification_time = os.path.getmtime(folder_path)
        
        access_time = datetime.fromtimestamp(last_access_time).strftime('%Y-%m-%d %H:%M:%S')
        modification_time = datetime.fromtimestamp(last_modification_time).strftime('%Y-%m-%d %H:%M:%S')

        meta_data = {
            'size': size,
            'last_access_time': access_time,
            'last_modification_time': modification_time,
            'number_of_sub_files': count['num_files'],
            'number_of_sub_folders': count['num_folders']
        }

        return meta_data
    
    except OSError as e:
        # Handle exceptions, if the folder doesn't exist
        print(f"Error: {e}")
        return None


def get_file_text(file_path: str) -> str:
    if file_path.split('.')[-1] == 'txt':
        with open(file_path, "r") as f:
            return f.read()

    text = textract.process(file_path)
    return text.decode("utf-8")


def hash_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        h = hashlib.new('sha256')

        # Read the file in chunks to handle large files
        chunk_size = 8192
        for chunk in iter(lambda: f.read(chunk_size), b''):
            h.update(chunk)

    return h.hexdigest()


def classify_document(document: Document):
    text = preprocess_document(get_file_text(document.file_path))

    # Perform document classification using zero-shot-classification generative AI model
    pipe = pipeline('zero-shot-classification')
    classification_result = pipe(text, candidate_labels=LABELS)

    # Update the classification label in the database
    document.classification_label = classification_result['labels'][0]
    document.save()


def preprocess_document(text: str) -> str:
    stemmer = nltk.stem.SnowballStemmer('english', ignore_stopwords=True)
    stop_words = list(set(stopwords.words('english')))
    # whitelist = set('abcdefghijklmnopqrstuvwxyz# ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    clean_text = text.encode('ascii', 'ignore').decode('ascii')
    clean_text = ''.join(i + ' ' for i in [stemmer.stem(word) for word in clean_text.lower().split() if word not in stop_words])

    return clean_text