from django.core.exceptions import ValidationError
def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2 MB limit
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed {limit} MiB.')
    return value