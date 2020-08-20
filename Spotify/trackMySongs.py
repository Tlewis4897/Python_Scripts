import spotipy.util as util
import spotipy
from collections import Counter

username = 
client_id =
client_secret = 
redirect_uri = 
scope = 

token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)
print(token)
myplaylistname = 'Most Played Songs'
sp = spotipy.Spotify(token)
print(sp)
trackPlaylists = []
playList = {}


def trackSongCount(user):
    playlists = user.user_playlists(#Enter your playlist ID)
    myPlaylists = playlists['items']
    for currentPlayLists in myPlaylists:
        trackPlaylists.append(currentPlayLists['name'])
    if myplaylistname not in trackPlaylists:
        t = user.user_playlist_create(username, myplaylistname, public=True, 
                                  description='Playlist with my popular songs')
    playlists2 = user.user_playlists(#Enter your playlist ID)
    print(playlists2)

        # playList[t['name']] = t['uri']
    print(playList)
    myPlaylistId = playList.get(myplaylistname)
    getPlaylistId = myPlaylistId.split(':')
    playlistId = getPlaylistId[2]
    x = user.user_playlist_tracks(user, playlistId, fields=None, limit=100, offset=0, market=None)
    d=(x['items'])
    myCurrentListSongs = []
    for i in d:
        myCurrentListSongs.append(i['track']['name'])
    myTracks = user.current_user_recently_played(limit=50, after=None,
                                                 before=None)
    mySongs = myTracks['items']
    mytrackuri = []
    for recentlyPlayed in mySongs:
        mytrackuri.append(recentlyPlayed['track']['uri'])
    uriId = Counter(mytrackuri)
    # y = Counter(myPlayedSongs)
    mostPlayedId = []
    for key, songID in uriId.items():
        if songID >= 3:
            getId = (key.split(':'))
            mostPlayedId.append(getId[2])
    for popularSongs in mostPlayedId:
        if popularSongs not in myCurrentListSongs:
            user.user_playlist_add_tracks(user, playlistId, mostPlayedId, position=None)
    print('Stop listening so much {}'.format(key))


trackSongCount(sp)
