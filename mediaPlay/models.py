from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class RockManager(models.Manager):
    def rockList(self):
        return self.filter(genre__iexact = "Rock")
    
class PopManager(models.Manager):
    def popList(self):
        return self.filter(genre__iexact = "Pop")

class Song(models.Model):
    track_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length= 100)
    artist = models.CharField(max_length = 100)
    album = models.CharField(max_length= 100, default='Single')
    genre = models.CharField(max_length= 100)
    lyrics = models.TextField()
    img = models.ImageField(upload_to='img')
    track = models.FileField(upload_to='track')
    objects = models.Manager()
    popSongs = PopManager()
    rockSongs = RockManager()

    # def __str__(self):
    #     return f"{self.title} - {self.artist}"
    
class Listener(models.Model):
    gen = [('Male', 'male'), ('Female', 'female'), ('Others','others')]
    lid = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 50, default="")
    last_name = models.CharField(max_length=50, default="")
    contact = models.PositiveBigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    email = models.EmailField(max_length=100, unique=True)
    address = models.TextField(max_length=500, default = "")
    gender = models.CharField(max_length = 20, choices=gen)
    profile_pic = models.ImageField(upload_to='user_profile_pic', default='user_profile_pic/guest.jpg')
    member = models.CharField(max_length=100, default="GUEST")
    username = models.CharField(max_length=50, default="", null=False, unique = True)
    password = models.CharField(max_length=16, default="")
    
class Playlist(models.Model):
    listener = models.ForeignKey(Listener, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)
    name = models.CharField(max_length=50, default="Liked Songs")

    def songs(self):
        return "\n".join([f"{song.title} - {song.artist}" for song in self.song.all()])
    
    def listener_name(self):
        return f"{self.listener.username}"


class Payment(models.Model):
    pid = models.CharField(primary_key=True, max_length=10)
    listener = models.ForeignKey(Listener, on_delete=models.DO_NOTHING)
    membership = models.CharField(max_length=50)
    amount = models.IntegerField()
    pdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listener.username} - {self.membership} - {self.pdate} // {self.pid}"
    
    
    
    
    