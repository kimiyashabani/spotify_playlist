import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
SPOTIPY_CLIENT_ID = "MY-CLIENT-ID"
SPOTIPY_CLIENT_SECRET = "MY-CLIENT-SECRET"
travel_to = input("Whcih year do you want to travel to? Type the date in this format: YYYY-MM-DD")
response = requests.get(f'https://www.billboard.com/charts/hot-100/{travel_to}/')
web_page = response.text
soup = BeautifulSoup(web_page, 'html.parser')
songs_names = soup.select('li ul li h3')
songs_names_list = [songs.getText().strip() for songs in songs_names]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="Billboard to spotify",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = travel_to.split("-")[0]
for song in songs_names_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{travel_to} Billboard 100", public=False)
playlist_id = playlist['id']
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)