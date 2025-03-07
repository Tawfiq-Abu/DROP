from django.db import models

class Contestant(models.Model):
    email = models.EmailField(unique=True)
    total_marks = models.IntegerField(default=0)

    class Meta:
        ordering = ['-total_marks']  # Orders by highest total_marks first<

    def __str__(self):
        return f"{self.email} - {self.total_marks}"

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Store files in "uploads/" folder
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Store upload timestamp

    def __str__(self):
        return self.file.name