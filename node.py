class Node:
    def __init__(self, track_id, artists, track_name, popularity, duration_ms, 
                 danceability, energy, loudness, instrumentalness, 
                 valence, tempo, track_genre):
        self.track_id = track_id
        self.artists = artists
        self.track_name = track_name
        self.popularity = popularity
        self.duration_ms = duration_ms
        self.danceability = danceability
        self.energy = energy
        self.loudness = loudness
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.tempo = tempo
        self.track_genre = track_genre
       
    # for print debugging purposes 
    def __repr__(self):
        return f"Node(track_id={self.track_id}, artists={self.artists}, track_name={self.track_name}, " \
               f"popularity={self.popularity}, duration_ms={self.duration_ms}, danceability={self.danceability}, " \
               f"energy={self.energy}, loudness={self.loudness}, " \
               f"instrumentalness={self.instrumentalness}, valence={self.valence}, tempo={self.tempo}, " \
               f"track_genre={self.track_genre})"
               
