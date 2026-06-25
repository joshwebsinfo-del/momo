"""
core/storage.py — Supabase Storage helper service.

Provides upload functions for each storage bucket with file validation.
All uploads return a public URL string.
"""

import uuid
import mimetypes
from django.conf import settings


def _get_supabase_client():
    """Lazily create and return a Supabase client."""
    from supabase import create_client
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def _upload_file(bucket: str, path: str, file_obj, content_type: str) -> str:
    """
    Upload a file to a Supabase Storage bucket.
    Returns the public URL of the uploaded file.
    """
    client = _get_supabase_client()
    data = file_obj.read()

    # Upload (upsert=True allows replacing existing files)
    client.storage.from_(bucket).upload(
        path=path,
        file=data,
        file_options={'content-type': content_type, 'upsert': 'true'},
    )

    # Return the public URL
    response = client.storage.from_(bucket).get_public_url(path)
    return response


def upload_memory_photo(file_obj, user_id: str) -> str:
    """Upload a memory photo. Max 10 MB."""
    if file_obj.size > settings.MAX_IMAGE_SIZE:
        raise ValueError('Image must be smaller than 10 MB.')

    allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
    content_type = file_obj.content_type
    if content_type not in allowed_types:
        raise ValueError('Only JPG, PNG, WebP, or GIF images are allowed.')

    ext = mimetypes.guess_extension(content_type) or '.jpg'
    filename = f'photos/{user_id}/{uuid.uuid4()}{ext}'
    return _upload_file(settings.SUPABASE_BUCKET_MEMORIES, filename, file_obj, content_type)


def upload_memory_video(file_obj, user_id: str) -> str:
    """Upload a memory video. Max 50 MB."""
    if file_obj.size > settings.MAX_VIDEO_SIZE:
        raise ValueError('Video must be smaller than 50 MB.')

    allowed_types = ['video/mp4', 'video/quicktime', 'video/webm', 'video/x-msvideo']
    content_type = file_obj.content_type
    if content_type not in allowed_types:
        raise ValueError('Only MP4, MOV, WebM, or AVI videos are allowed.')

    ext = mimetypes.guess_extension(content_type) or '.mp4'
    filename = f'videos/{user_id}/{uuid.uuid4()}{ext}'
    return _upload_file(settings.SUPABASE_BUCKET_MEMORIES, filename, file_obj, content_type)


def upload_voice_message(file_obj, user_id: str) -> str:
    """Upload a voice message audio file. Max 20 MB."""
    if file_obj.size > settings.MAX_AUDIO_SIZE:
        raise ValueError('Audio must be smaller than 20 MB.')

    allowed_types = ['audio/webm', 'audio/ogg', 'audio/mpeg', 'audio/wav', 'audio/mp4']
    content_type = file_obj.content_type or 'audio/webm'
    if content_type not in allowed_types:
        raise ValueError('Only WebM, OGG, MP3, or WAV audio files are allowed.')

    ext = mimetypes.guess_extension(content_type) or '.webm'
    filename = f'{user_id}/{uuid.uuid4()}{ext}'
    return _upload_file(settings.SUPABASE_BUCKET_VOICE, filename, file_obj, content_type)


def upload_voice_blob(blob_bytes: bytes, user_id: str, content_type: str = 'audio/webm') -> str:
    """Upload a raw audio blob (from browser MediaRecorder). Max 20 MB."""
    if len(blob_bytes) > settings.MAX_AUDIO_SIZE:
        raise ValueError('Audio must be smaller than 20 MB.')

    ext = mimetypes.guess_extension(content_type) or '.webm'
    filename = f'{user_id}/{uuid.uuid4()}{ext}'

    client = _get_supabase_client()
    client.storage.from_(settings.SUPABASE_BUCKET_VOICE).upload(
        path=filename,
        file=blob_bytes,
        file_options={'content-type': content_type, 'upsert': 'true'},
    )
    return client.storage.from_(settings.SUPABASE_BUCKET_VOICE).get_public_url(filename)


def upload_profile_picture(file_obj, user_id: str) -> str:
    """Upload a profile picture. Max 10 MB."""
    if file_obj.size > settings.MAX_IMAGE_SIZE:
        raise ValueError('Image must be smaller than 10 MB.')

    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    content_type = file_obj.content_type
    if content_type not in allowed_types:
        raise ValueError('Only JPG, PNG, or WebP images are allowed.')

    # Use a deterministic path so re-uploading replaces the old picture
    ext = mimetypes.guess_extension(content_type) or '.jpg'
    filename = f'{user_id}/avatar{ext}'
    return _upload_file(settings.SUPABASE_BUCKET_PROFILES, filename, file_obj, content_type)


def upload_timeline_image(file_obj, user_id: str) -> str:
    """Upload a timeline event image. Max 10 MB."""
    if file_obj.size > settings.MAX_IMAGE_SIZE:
        raise ValueError('Image must be smaller than 10 MB.')

    allowed_types = ['image/jpeg', 'image/png', 'image/webp']
    content_type = file_obj.content_type
    if content_type not in allowed_types:
        raise ValueError('Only JPG, PNG, or WebP images are allowed.')

    ext = mimetypes.guess_extension(content_type) or '.jpg'
    filename = f'timeline/{user_id}/{uuid.uuid4()}{ext}'
    return _upload_file(settings.SUPABASE_BUCKET_MEMORIES, filename, file_obj, content_type)
