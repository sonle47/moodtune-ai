from urllib.parse import quote


def add_search_links(playlist):
    for track in playlist:
        query = quote(f"{track['title']} {track['artist']}")
        track["search_url"] = f"https://www.youtube.com/results?search_query={query}"
    return playlist