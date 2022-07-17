from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from youtube_search import YoutubeSearch
from ytmusicapi import YTMusic
import tqdm
ytmusic = YTMusic('headers.json')
# PLAYLISTS = [['Accidental','https://open.spotify.com/playlist/0zJ8hC8YJOcHYuk5nMPFm8?si=U6Kyom3XQ32reSuVgl2uhA', "PL59eqqQABruMQOPlUVcVsIid685ZdwDjf"],
# ['TimePass','https://open.spotify.com/playlist/6gADLrLFK1kXgEEOsENi1c', "PL59eqqQABruMSx6VSy1hbkBhG4XwtgSuy"],
# ['CHILLS','https://open.spotify.com/playlist/3zs3QOLX8bASY5oV2dmEQw', 'PL59eqqQABruN3GyAPiPnQ6Jq-TngWjT-Y'],
# ['Programming & Coding Music','https://open.spotify.com/playlist/6vWEpKDjVitlEDrOmLjIAj', 'PL59eqqQABruNew5O0cRvomfbU6FI0RGyl'],
PLAYLISTS = [['Tamil','https://open.spotify.com/playlist/37i9dQZF1DX2x1COalpsUi',None],
['Maveric', 'https://open.spotify.com/playlist/0TI9gUMwv2DimLzEaofH44',None],
['English Melodies', 'https://open.spotify.com/playlist/1x2wjbiw9ZAVa1OQLNbaNH',None]


 #https://open.spotify.com/playlist/37i9dQZF1DX2x1COalpsUi?si=6ed63a486e144585
# ['Spanish','https://open.spotify.com/playlist/75QJ1JeFaeSm0uH1znWxb0?si=Lt4kd-RARBu2TQz35RAQiQ', 'PL59eqqQABruM3TLAGthvgW10c1R6omGwq']
]
client_credentials_manager = SpotifyClientCredentials(client_id='17c2183917474c9ca53085e93a30bb83',
                client_secret='fe0691cee0314448b731ffe483481bf5')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
print('connected to spotify.....')


CONTAINER = []
for playlist in tqdm.tqdm(PLAYLISTS):
    Name,Link,playlistid = playlist
    playlistcard = []
    count = 0
    PlaylistLink = "https://www.youtube.com/watch_videos?video_ids="
    for i in (sp.playlist_tracks(Link)['items']):
        if count == 50:
            break
        try:
            song = i['track']['name'] + i['track']['artists'][0]['name']
            print('got the song',song)
            songdic = (YoutubeSearch(song, max_results=1).to_dict())[0]
            playlistcard.append([songdic['thumbnails'][0],songdic['title'],songdic['channel'],songdic['id']])
            PlaylistLink += songdic['id'] + ','
        except:
            continue
        count += 1

    from urllib.request import urlopen
    req = urlopen(PlaylistLink)
    PlaylistLink = req.geturl()
    print(PlaylistLink)
    PlaylistId = PlaylistLink[PlaylistLink.find('list')+5:]
    print(PlaylistId, 'id is---------')

    CONTAINER.append([Name,playlistcard,playlistid])
print('created playlists.....')
import json

json.dump(CONTAINER,open('card.json', 'w'),indent = 6) 
