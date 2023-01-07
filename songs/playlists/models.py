from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)

    def __str__(self):
        return self.title + " by "  + self.artist
    

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)

    def __str__(self) -> str:
        return self.name
    def no_of_songs(self):
        return len(self.songs.all())
    

    
# Create your models here.
