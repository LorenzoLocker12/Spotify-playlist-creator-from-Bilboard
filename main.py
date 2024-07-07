import os
from bs4 import BeautifulSoup
import requests as re
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
username = os.getenv("USERNAME")

# Soup
year = input("Enter the year you'd like to get the top 100 music: ")

response = re.get(f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/")
soup = BeautifulSoup(response.text, "html.parser")

# Titles
raw_titles = soup.find_all("h3", id="title-of-a-story", class_="c-title")
raw_titles = raw_titles[:100]
clean_titles = [(title.get_text()).strip() for title in raw_titles]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user = sp.current_user()["id"]

titles_uris = []
for i in clean_titles:
    search = sp.search(q=f"track:{i} year:{year}", type="track")
    print(search)
    try:
        uri = search["tracks"]["items"][0]["uri"]
        titles_uris.append(uri)
    except IndexError:
        pass


playlist = sp.user_playlist_create(user=user, name=f"Best Musics from {year}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=titles_uris)