import os
from pathlib import Path

import bleach
import requests
from decouple import config
from django.core.files.uploadedfile import UploadedFile


def sanitize_text(value):
    if not value:
        return ""
    return bleach.clean(
        value,
        tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a'],
        attributes={'a': ['href', 'target']},
        protocols=['http', 'https', 'mailto'],
        strip=True,
    )


def validate_upload(file_obj, allowed_types, max_size_mb):
    if not isinstance(file_obj, UploadedFile):
        raise ValueError('Invalid upload.')
    if file_obj.size > max_size_mb * 1024 * 1024:
        raise ValueError(f'File exceeds {max_size_mb}MB limit.')
    if file_obj.content_type not in allowed_types:
        raise ValueError('Unsupported file type.')


def upload_to_storage(file_obj, bucket_name, folder=''):
    if not file_obj:
        return None
    storage_url = config('SUPABASE_STORAGE_URL', default='').strip()
    storage_key = config('SUPABASE_STORAGE_KEY', default='').strip()
    if storage_url and storage_key:
        file_name = getattr(file_obj, 'name', 'upload.bin')
        object_name = f"{folder}/{file_name}".strip('/')
        url = f"{storage_url.rstrip('/')}/object/{bucket_name}/{object_name}"
        headers = {
            'apikey': storage_key,
            'Authorization': f'Bearer {storage_key}',
        }
        response = requests.post(url, headers=headers, data=file_obj.read(), timeout=60)
        if response.ok:
            return url
    return None
