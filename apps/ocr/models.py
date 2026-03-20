import os
from django.db import models


def upload_to(instance, filename):
    """Store uploads in media/uploads/ with original filename."""
    return os.path.join('uploads', filename)


class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to=upload_to)
    original_filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.original_filename} ({self.status})"

    @property
    def file_extension(self):
        _, ext = os.path.splitext(self.original_filename)
        return ext.lower()

    @property
    def is_pdf(self):
        return self.file_extension == '.pdf'

    @property
    def is_image(self):
        return self.file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']


class OCRResult(models.Model):
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name='result',
    )
    extracted_text = models.TextField(blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.document.original_filename}"
