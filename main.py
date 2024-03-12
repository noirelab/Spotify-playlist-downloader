import requests
import os
from pytube import YouTube
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getTracks(playlist_id, output_file):
    client_id = '644b1df8c9b34f19b9eacf684f44d4c2'
    client_secret = '357800ac67314c0ab4a7936cca3cb1d0'
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # gets all the tracks on the playlist, if there is a second page, it'll advance on its own ['nexst'] | dictionaries sucks!
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
        
    # writes on a file the track and artist's name | dictionaries sucks! 2x
    with open(output_file, 'w', encoding='utf-8') as file:
        for track in tracks:
            track_name = track['track']['name']
            artist = track['track']['artists'][0]['name']
            file.write(f"{artist} - {track_name}\n")

def searchYoutube(query):
    api_key = "AIzaSyB8LH3Us2FujNWtcsfl1dkbhhoFnJEKP4c"

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # dictionaries sucks! 3x
    if 'items' in data and data['items']:
        video_id = data['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return "no results found"

def donwloadYoutubeMP3(output_folder, result):
    yt = YouTube(result)
    
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(output_folder, filename=yt.title + '.mp3')
    
    return os.path.join(output_folder, yt.title + '.mp3')

if __name__ == "__main__":
    playlist_id = '37i9dQZF1DZ06evO2lVf2b'
    output_file = 'playlist_tracks.txt'
    output_folder = 'downloads'
    input_file = r"C:\Users\kaiqu\2024\project\playlist_tracks.txt"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # getTracks(playlist_id, output_file)
    
    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            query = line.strip()
            result = searchYoutube(query)
            donwloadYoutubeMP3(output_folder, result)