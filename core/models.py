from django.db import models


class Document(models.Model):
    file_path = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    classification_label = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # TODO make hash and file_path unique together