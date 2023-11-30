import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse, request

from rest_framework.decorators import api_view


@api_view(['GET'])
# @login_required
def index(request):
    folder_path = request.GET.get('path')
    folder_path = os.path.join('../data/', folder_path)

    # Validate folder path
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return JsonResponse({'error': 'Invalid folder path'})

    # Get list of files in the folder
    files = os.listdir(folder_path)
    return JsonResponse({'files': files, 'message': 'Folder insight processed successfully'})