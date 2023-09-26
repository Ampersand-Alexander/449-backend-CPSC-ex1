import requests

# Define the GraphQL API endpoint & header since its the same
graphql_url = 'http://localhost:4000/graphql'


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_AUTH_TOKEN'
}


def part1graphql():
    print("\npart 1 Albums by the artist Red Hot Chili Peppers with GraphQL")

    query = """
    {
        artist(where: { Name: "Red Hot Chili Peppers"}){
            artistId,
            albums{
                albumId
                title
            }
        }
    }
    """

    graphql_request = {
        'query': query
    }

    response = requests.post(graphql_url, json=graphql_request, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print("GraphQL query errors:", data['errors'])
        else:
            for album in data['data']['artist']['albums']:
                print(album['title'])
    else:
        print("Failed to fetch data from GraphQL API. Status code:", response.status_code)

def part1rest():
    print("\npart 1 Albums by the artist Red Hot Chili Peppers with REST API")
    #get artist Id to use for later

    artist_name = "Red Hot Chili Peppers"
    rest_url = f"http://localhost:8000/api/tables/artists/rows?_schema=ArtistId&_filters=name:{artist_name}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            artist_id =  data['data'][0]['ArtistId']
            print("got id of ", artist_id)
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

    #use artist Id to find associated albums

    rest_url = f"http://localhost:8000/api/tables/albums/rows?_filters=ArtistId:{artist_id}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            for album in data['data']:
                print(album['Title'])
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

def part2graphql():
    print("\npart 2 Genres associated with the artist U2 with graphql")

    query = """
    {
        artists(where: { Name : "U2" }){
            albums{
                tracks{
                    genre{
                        genreId
                        name
                    }
                }
            }
        }
    }
    """

    graphql_request = {
        'query': query
    }


    response = requests.post(graphql_url, json=graphql_request, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print("GraphQL query errors:", data['errors'])
        else:
            unique_genres = set()
            for artist in data['data']['artists']:
                for album in artist['albums']:
                    for track in album['tracks']:
                        if track['genre']['name'] not in unique_genres:
                            genre=track['genre']['name']
                            unique_genres.add(genre)
                            print(genre)
    else:
        print("Failed to fetch data from GraphQL API. Status code:", response.status_code)

def part2rest():
    print("\npart 2 with REST API")
    #get artist Id to use for later

    artist_name = "U2"
    rest_url = f"http://localhost:8000/api/tables/artists/rows?_schema=ArtistId&_filters=name:{artist_name}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            artist_id =  data['data'][0]['ArtistId']
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

    #use artist Id to find associated albums

    rest_url = f"http://localhost:8000/api/tables/albums/rows?_filters=ArtistId:{artist_id}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            albumslist = set()
            for album in data['data']:
                albumslist.add(album['AlbumId'])
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

    #use album Id to find genres from tracks
    for albumid in albumslist:
        rest_url = f"http://localhost:8000/api/tables/tracks/rows?_filters=AlbumId:{albumid}"
        response = requests.get(rest_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            if 'error' in data:
                print("API Error:", data['error'])
            else:
                genreindeed = set()
                for genre in data['data']:
                    if genre['GenreId'] not in genreindeed:
                        genreindeed.add(genre['GenreId'])
        else:
            print("Failed to fetch data from REST API. Status code:" , response.status_code)
    #use genre Id to find genres name
    for genreid in genreindeed:
        rest_url = f"http://localhost:8000/api/tables/genres/rows?_filters=GenreId:{genreid}"
        response = requests.get(rest_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            if 'error' in data:
                print("API Error:", data['error'])
            else:
                for genrename in data['data']:
                    print(genrename['Name'])
        else:
            print("Failed to fetch data from REST API. Status code:" , response.status_code)

    

def part3graphql():
    print("\npart 3 Names of tracks on the playlist “Grunge” and their associated artists and albums with GraphQL")

    query = """
    {
        playlists(where: { Name : "Grunge" }){
                tracks{
            name
            album{
                title
                artist{
                name
                }
            }
            }
        }
    }
    """

    graphql_request = {
        'query': query
    }


    response = requests.post(graphql_url, json=graphql_request, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print("GraphQL query errors:", data['errors'])
        else:
            for playlist in data['data']['playlists']:
                for track in playlist['tracks']:
                    name = track['name']
                    album = track['album']['title']
                    artist = track['album']['artist']['name']
                    print(f"{name} by {artist}, {album}")
    else:
        print("Failed to fetch data from GraphQL API. Status code:", response.status_code)

def part3rest():
    print("\npart 3 with REST API")
    #get playlist id

    name = "Grunge"
    rest_url = f"http://localhost:8000/api/tables/playlists/rows?_page=1&_limit=10&_filters=Name:{name}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            playlist_id =  data['data'][0]['PlaylistId']
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)
    
    #get track id

    rest_url = f"http://localhost:8000/api/tables/playlist_track/rows?_page=1&_limit=10&_filters=PlaylistId:{playlist_id}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            track_id =  data['data'][0]['TrackId']
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

    #print track name
  
    rest_url = f"http://localhost:8000/api/tables/tracks/rows?_page=1&_limit=10&_filters=TrackId:{track_id}"
    response = requests.get(rest_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            print("API Error:", data['error'])
        else:
            print(data['data'][0]['Name'])
    else:
        print("Failed to fetch data from REST API. Status code:", response.status_code)

    

if __name__ == "__main__":
    part1graphql()
    part1rest()
    part2graphql()
    part2rest()
    part3graphql()
    part3rest()