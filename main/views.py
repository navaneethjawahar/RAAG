from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import playlist_user , recommended_song
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
import json
from main.utils import recommend_songs
from django.views.decorators.csrf import csrf_protect

f = open('card.json', 'r')
CONTAINER = json.load(f)

@login_required(login_url="login/")
def default(request):
    global CONTAINER
    if request.method == 'POST':
        add_playlist(request)
        add_recommendation(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})

def signup(request):
    context= {'username':True,'email':True}
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')



        if (username,) in User.objects.values_list("username",) :
            context['username'] = False
            return render(request,'signup.html',context)

        elif (email,) in User.objects.values_list("email",):
            context['email'] = False
            return render(request,'signup.html',context)

        playlist_user.objects.create(username=username)
        new_user = User.objects.create_user(username,email,password)
        new_user.save()
        login(request,new_user)
        return redirect('/')
    return render(request,'signup.html',context)

@csrf_protect
def login_auth(request):
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(User.objects.values_list("password",))

        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return redirect('/')

        else:
            # No backend authenticated the credentials
            context= {'case':False}
            return render(request,'login.html',context)


    context= {'case':True}
    return render(request,'login.html',context)



def logout_auth(request):
    logout(request)
    return redirect('/login')

@login_required(login_url="login/")
def playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        add_recommendation(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})

@csrf_protect
@login_required(login_url="login/")
def recommendation(request):
    # if request.user.is_anonymous:
    #     return redirect('/login')
    cur_user = playlist_user.objects.get(username = request.user)
    try:
        song = request.GET.get('song')
        song = cur_user.recommended_song_set.get(song_title=song)
        song.delete()
    except:
      pass
    if request.method == 'POST':
        # print('caught the song -' )
        add_playlist(request)
        add_recommendation(request)
        return HttpResponse("")
    if request.method == 'PUT':
        print('Got the request in django')
        video_data = json.loads(request.body)
        v_id = video_data.get('videoId')
        liked = video_data.get('liked')
        save_recommendation_response(request,v_id,liked)
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.recommended_song_set.all()
    # print(user_playlist)
    # print(list(playlist_row)[0].song_title)
    return render(request, 'recommendation.html', {'song':song,'user_playlist':user_playlist})

@login_required(login_url="login/")
def search(request):
  if request.method == 'POST':

    add_playlist(request)
    add_recommendation(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})




def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])


def save_recommendation_response(request,videoId,liked):
    curr_song = recommended_song.objects.get(song_youtube_id = videoId)
    curr_song.recommendation_liked = liked
    curr_song.save()
    print('data saved successfully')

def add_recommendation(request):
    cur_user = playlist_user.objects.get(username = request.user)
    new_song = request.POST['title']
    print(new_song,'recccc')

    # print(dict(request.POST).keys())
    # print(new_song)

    # if (new_song,) not in cur_user.recommended_song_set.values_list('song_title', ):
    song_dict = {"name": new_song,"year":2000}
    # print('recommended songs - ', recommend_songs([song_dict]))
    rec_songs = recommend_songs([song_dict])
    # print(rec_songs)
    for song in rec_songs:
        songdic = (YoutubeSearch(song.get('name'), max_results=1).to_dict())[0]
        # print(songdic)
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.recommended_song_set.create(song_title=songdic.get('title'),song_dur=songdic.get('duration'),
        song_albumsrc = song__albumsrc,
        song_channel=songdic.get('channel'), song_date_added=request.POST['date'],song_youtube_id=songdic.get('id')) #song_dict.get('duration')