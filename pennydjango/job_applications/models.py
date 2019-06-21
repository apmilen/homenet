from django.db import models

from job_applications.utils import resume_path, validate_file_extension
from job_applications.constants import JOB_POSITION


class JobApplication(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=50)
    current_company = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255, choices=JOB_POSITION)
    resume = models.FileField(
        upload_to=resume_path, 
        validators=[validate_file_extension]
    )
