import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse, request

from rest_framework.decorators import api_view

from core.utils import get_folder_meta_data, hash_file, classify_document, build_tree
from core.models import Document


@api_view(['GET'])
# @login_required
def analyze_folder(request):
    folder_path = request.GET.get('path')
    folder_path = os.path.join('../data/', folder_path)

    # Validate folder path
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return JsonResponse({'error': 'Invalid folder path'})

    data = build_tree(folder_path)
    data['meta'] = get_folder_meta_data(folder_path)

    return JsonResponse({'data': data, 'message': 'Folder insight processed successfully'})


@api_view(['GET'])
def document_classification(request):
    file_path = request.GET.get('path')
    file_path = os.path.join('../data/', file_path)

    print(file_path)

    # Validate folder path
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'Invalid file path'})

    hash = hash_file(file_path)

    document, created = Document.objects.get_or_create(
        file_path=file_path,
        hash=hash
    )

    if created or not document.classification_label:
        classify_document(document)

    data = {
        'file_path': document.file_path,
        'hash': document.hash,
        'label': document.classification_label
    }

    return JsonResponse({'data': data, 'message': 'Document classified successfully'})