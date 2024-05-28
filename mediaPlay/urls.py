from django.urls import path
from .views import Lyrics, Register, EditProfile, UploadSong
from . import views

urlpatterns = [
    path('', views.index, name = "index"),
    path('playnow/<int:track>', views.playnow, name = "playnow"),
    path('membership/', views.membership, name = "membership"),
    path('lyrics/<int:pk>', Lyrics.as_view(), name = "lyrics"),
    path('register/', Register.as_view(), name = "register"),
    path('login/', views.login_user, name = "login"),
    path('logout/', views.logout_user, name = "logout"),
    path('add_to_liked_songs/<int:track>', views.add_to_liked_songs, name = "add_to_liked_songs"),
    path('playlist/', views.playlist, name = "playlist"),
    path('search/', views.search, name = "search"),
    path('upload_your_own/', UploadSong.as_view(), name = 'upload_your_own'),
    path('makePayment/<int:amount>', views.makePayment, name = "makePayment"),
    path('editProfile/<int:pk>', EditProfile.as_view(), name = "editProfile"),
    path('sendMail/<str:user>', views.sendUserMail, name = "sendMail")
]