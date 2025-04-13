from django.db import models

class AudioBook(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image = models.ImageField(upload_to='audio_images/', null=True, blank=True)
    audio_file = models.FileField(upload_to='audio_files/')
    language = models.CharField(max_length=50, default='English')

    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('nonfiction', 'Non-fiction'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('sci-fi', 'Sci-Fi'),
        ('romance', 'Romance'),
        ('history', 'History'),
    ]
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='')

    def __str__(self):
        return self.title
