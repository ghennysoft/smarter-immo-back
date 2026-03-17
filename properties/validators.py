from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image_file(file):
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)
    allowed_types = getattr(settings, 'ALLOWED_IMAGE_TYPES', ['image/jpeg', 'image/png', 'image/webp'])

    if file.size > max_size:
        raise ValidationError(f'La taille du fichier ne doit pas dépasser {max_size // (1024 * 1024)} Mo.')

    if file.content_type not in allowed_types:
        raise ValidationError(f'Type de fichier non autorisé. Types acceptés : {", ".join(allowed_types)}')
