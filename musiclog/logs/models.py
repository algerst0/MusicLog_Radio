from django.db import models

from django.db import models

class MusicLog(models.Model):
    timestamp = models.DateTimeField()
    song_title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    duration = models.CharField(max_length=5)  # MM:SS format
    isrc = models.CharField(max_length=12, unique=True)
    program = models.CharField(max_length=255)
    dj = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.song_title} by {self.artist} on {self.program} at {self.timestamp}"
