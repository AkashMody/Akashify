from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView, View, CreateView
import django.db
import random
from django.urls import reverse_lazy
import razorpay
from .models import Song, Listener, Playlist, Payment
from .forms import ListenerForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail

# Create your views here.

def index(req):
    try:
        songs = Song.objects.all()
        pop_songs = Song.popSongs.popList()
        rock_songs = Song.rockSongs.rockList()
        active_user = req.session.get('active_user')
        if active_user is None:
            return redirect('/login')
        else:
            listener = Listener.objects.get(username = active_user)
            liked_songs_list = Playlist.objects.filter(name = "Liked Songs", listener = listener)
            # print(liked_songs_list)
            liked_songs = []
            for liked in liked_songs_list:
                liked_songs.append(liked.song.all())
            default_playlist = []
            for tracks in liked_songs:
                for song in tracks:
                    default_playlist.append(song)
            # print(default_playlist)
            songtext = {"songs": songs, "poplist": pop_songs, "rocklist": rock_songs, "active_user": active_user, "listener": listener, "liked_songs": default_playlist}
            return render(req, "index.html", songtext)
    except Listener.DoesNotExist:
        return redirect('/login')
    except Playlist.DoesNotExist:
        default_playlist = None
        songtext = {"songs": songs, "poplist": pop_songs, "rocklist": rock_songs, "active_user": active_user, "listener": listener, "liked_songs": default_playlist}
        return render(req, "index.html", songtext)

def membership(req):
    active_user = req.session.get("active_user")
    if active_user is None:
            return redirect('/login')
    else:
        listener = Listener.objects.get(username = active_user)
        # print(listener)
        songtext = {"listener": listener}
        return render(req, "membership.html", songtext)

class Lyrics(DetailView):
    model = Song
    template_name = "lyrics.html"
    
def playnow(req, track):
    nowplay = Song.objects.get(track_id = track)
    songtext = {"title": nowplay.title,
                "artist": nowplay.artist,
                "img": nowplay.img.url,
                "track": nowplay.track.url}
    return JsonResponse(songtext)

def add_to_liked_songs(req, track):
    songtext = {}
    active_user = req.session.get("active_user")
    try:
        listener = Listener.objects.get(username = active_user)
        song = Song.objects.get(track_id = track)
        liked_song = Playlist.objects.get(listener = listener, song = song)
        liked_song.delete()
        songtext["isAdded"] = False        
        return JsonResponse(songtext)
    except Playlist.DoesNotExist:
        playlist = Playlist(listener = listener)
        playlist.save()
        playlist.song.add(song)
        playlist.save()
        songtext["isAdded"] = True
        return JsonResponse(songtext)

def playlist(req):
    active_user = req.session.get("active_user")
    listener = Listener.objects.get(username = active_user)
    liked_songs_list = Playlist.objects.filter(name = "Liked Songs", listener = listener)
    # print(liked_songs_list)
    liked_songs = []
    for liked in liked_songs_list:
        liked_songs.append(liked.song.all())
    default_playlist = []
    for tracks in liked_songs:
        for song in tracks:
            default_playlist.append(song)
    songtext = {}
    songtext['listener'] = listener
    songtext['playlist'] = default_playlist
    songtext['active_user'] = active_user
    return render(req, 'playlist.html', songtext)
    
def search(req):
    if req.method == 'POST':
        try:
            searchQuery = req.POST["search"]
            print("Search Query => ", searchQuery)
            songs = Song.objects.filter(Q(title__icontains = searchQuery) | Q(artist__icontains = searchQuery) | Q(lyrics__contains = searchQuery) | Q(genre__icontains = searchQuery))
            print(songs)
            pop_songs = Song.popSongs.popList()
            rock_songs = Song.rockSongs.rockList()
            active_user = req.session.get('active_user')
            if active_user is None:
                return redirect('/login')
            else:
                listener = Listener.objects.get(username = active_user)
                liked_songs_list = Playlist.objects.filter(name = "Liked Songs", listener = listener)
                # print(liked_songs_list)
                liked_songs = []
                for liked in liked_songs_list:
                    liked_songs.append(liked.song.all())
                default_playlist = []
                for tracks in liked_songs:
                    for song in tracks:
                        default_playlist.append(song)
                # print(default_playlist)
                songtext = {"songs": songs, "poplist": pop_songs, "rocklist": rock_songs, "active_user": active_user, "listener": listener, "liked_songs": default_playlist}
                return render(req, "index.html", songtext)
        except Listener.DoesNotExist:
            return redirect('/login')
        except Playlist.DoesNotExist:
            default_playlist = None
            songtext = {"songs": songs, "poplist": pop_songs, "rocklist": rock_songs, "active_user": active_user, "listener": listener, "liked_songs": default_playlist}
            return render(req, "index.html", songtext)
    else: return redirect("/")

class UploadSong(CreateView):
    model = Song
    fields = "__all__"
    template_name = "song.html"
    success_url = reverse_lazy('index')

def makePayment(req, amount):
    active_user = req.session.get("active_user")
    listener = Listener.objects.get(username = active_user)
    pid = random.randrange(1000, 9999)
    pid = str(pid)
    if amount == 100: membership = "PREMIUM INDIVIDUAL"
    elif amount == 200: membership = "PREMIUM FAMILY"
    elif amount == 50: membership = "PREMIUM STUDENT"
    else: membership = "GUEST"
    Payment.objects.create(pid = pid, listener = listener, membership = membership, amount = amount)
    client = razorpay.Client(auth=("rzp_test_hdRXvVm9I26QLq", "YkTWZmn4g9R0axiwoaBlnBZf"))
    data = { "amount": amount * 100, "currency": "INR", "receipt": pid }
    payment = client.order.create(data=data)
    made_payment = Payment.objects.get(pid = pid)
    print("Payment: ", made_payment)
    listener_new = Listener.objects.filter(username = active_user)
    print(listener_new)
    listener_new.update(member = membership)
    updated_member = Listener.objects.get(username = active_user)
    songtext = {}
    songtext['data'] = payment
    songtext['listener'] = updated_member
    songtext['payment'] = made_payment
    # print(payment)
    return render(req, "payment.html", songtext)

class Register(View):
    def get(self, req):
        form = ListenerForm()
        return render(req, 'register.html', {'form': form})
    
    def post(self, req):
        form = ListenerForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "User Created Successfully!")
            return redirect('/login')
        else:
            messages.error(req, form.errors.as_data())
        return render(req, "register.html", {"form": form})
    
class EditProfile(UpdateView):
    model = Listener
    fields = ("first_name", "last_name", "gender", "contact", "email", "address", "profile_pic")
    template_name = 'register.html'
    success_url = reverse_lazy('index')
    # def get(self, req, pk):
    #     data = Listener.objects.get(lid = pk)
    #     form = ListenerForm(instance= data)
    #     return render(req, "register.html", {'form': form})

    # def post(self, req, pk):
    #     data = Listener.objects.get(lid = pk)
    #     form = ListenerForm(req.POST, instance=data)
    #     if form.is_valid():
    #         form.save()
    #         for msg in messages:
    #             del msg
    #         messages.success(req, "User Created Successfully!")
    #         return redirect('/')
    #     else:
    #         for msg in messages:
    #                 del msg
    #         messages.error(req, form.errors.as_data())
    #     return render(req, "register.html", {'form': form})
    
def sendUserMail(req, user):
    print(user)
    listener = Listener.objects.get(username = user)
    if listener.member == "GUEST":
        msg = f"Membership Cancelled! You are now a GUEST"
    else:
        msg = f"Congratulations! you are now a {listener.member}"
    send_mail(
    "Member Access",
    f"Congratulations!! you are now a {listener.member} of Akashify",
    "mody.akash0808@gmail.com",
    [f"{listener.email}"],
    fail_silently=False,)
    messages.success(req, msg)    
    return redirect("/")

    
def login_user(req):
    if req.method == "GET":
        return render(req, 'login.html')
    else:
        try:            
            username = req.POST["uname"]
            password = req.POST["upass"]
            listener = Listener.objects.get(username = username)
            if listener.username == username and listener.password == password:
                req.session['active_user'] = username
                messages.success(req, "You're logged in successfully!!")
                return redirect("index")
            else:
                messages.error(req, "There was an error, Please try again!!")
                return redirect("login")
        except Listener.DoesNotExist:
            messages.error(req, "This user does not exist.")
            return redirect("login")
            
        
def logout_user(req):
    del req.session['active_user']
    messages.success(req, "You have logged out successfully! ")
    return redirect("/login")
        



