import requests
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
def get_token(clientId,clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    headers['Authorization'] = "Basic " + base64Message
    data['grant_type'] = "client_credentials"
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']
    return token

def get_track_recommendations(seed_tracks,token):
    limit = 10
    # USING THIS WEBSITE TO GET API
    
    # https://developer.spotify.com/console/get-recommendations/?limit=20&market=&seed_artists=&seed_genres=&seed_tracks=&min_acousticness=&max_acousticness=&target_acousticness=&min_danceability=&max_danceability=&target_danceability=&min_duration_ms=&max_duration_ms=&target_duration_ms=&min_energy=&max_energy=&target_energy=&min_instrumentalness=&max_instrumentalness=&target_instrumentalness=&min_key=&max_key=&target_key=&min_liveness=&max_liveness=&target_liveness=&min_loudness=&max_loudness=&target_loudness=&min_mode=&max_mode=&target_mode=&min_popularity=&max_popularity=&target_popularity=&min_speechiness=&max_speechiness=&target_speechiness=&min_tempo=&max_tempo=&target_tempo=&min_time_signature=&max_time_signature=&target_time_signature=&min_valence=&max_valence=&target_valence=
    recUrl = f"https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={seed_tracks}"


    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=recUrl, headers=headers)
    return res.json()

def song_recomdation_vis(reco_df):
    plt.figure(figsize=(15, 6), facecolor=(.9, .9, .9))   
    reco_df['duration_min'] = round(reco_df['duration_ms'] / 1000, 0)
    reco_df["popularity_range"] = reco_df["popularity"] - (reco_df['popularity'].min() - 1) 

    x = reco_df['name']
    y = reco_df['duration_min']
    s = reco_df['popularity_range']*50
        
    color_labels = reco_df['explicit'].unique()
    rgb_values = sns.color_palette("Set1", 8)
    color_map = dict(zip(color_labels, rgb_values))

    plt.scatter(x, y, s, alpha=0.7, c=reco_df['explicit'].map(color_map))
    plt.xticks(rotation=90)
    plt.legend()
    # show the graph
    plt.show()
    st.pyplot(plt)


def save_album_img(img_url,track_id):
    r=requests.get(img_url)
    open('img/'+track_id+'.jpg',"wb").write(r.content)

def get_album_img(track_id):
    return Image.open('img/'+track_id+'.jpg')
