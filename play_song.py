import webbrowser
import sys
import urllib.parse

# Keyword mapping
keyword_songs = {
    "my first song": "space chess",
    "my second song": "kompa passion"
}

def play_song_on_youtube(song_name):
    # Check for special keyword phrases
    lower_song_name = song_name.lower()
    if lower_song_name in keyword_songs:
        query = keyword_songs[lower_song_name]
    else:
        query = song_name

    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open(url)
    print(f"🔍 Opened YouTube search for: {query}")

if __name__ == "__main__":
    song_name = " ".join(sys.argv[1:])
    if song_name:
        play_song_on_youtube(song_name)
    else:
        print("Please provide a song name.")
