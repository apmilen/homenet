import os
import random

from django.core.exceptions import ValidationError


def validate_pdf_file(file):
    try:
        file_extension = os.path.splitext(file.name)[1].lower()
    except TypeError:
        pass

    if file_extension != '.pdf':
        raise ValidationError(
                ('Invalid file extension'),
        )


def resume_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    return '/'.join([f"{randomstr}{file_extension}"])
