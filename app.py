from lib2to3.pgen2 import token
from matplotlib import image
from sklearn import feature_selection
import streamlit as st
from tkinter.messagebox import NO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="93904d674b094e5095c70810366f6410",
                                                           client_secret="11d75b7e2b384b53a7d02f283fa68238"))
import pandas as pd
import polar_plot
C_ID = '93904d674b094e5095c70810366f6410'
C_SCR = '11d75b7e2b384b53a7d02f283fa68238'
import song_recomandation

st.header('Spotify App (streamlit)')
# st.sidebar.write('sideba')
all_choice = ['Songs/track', 'Artists', 'Album']
selected_search = st.sidebar.selectbox("Select Your Choice :", all_choice)
# st.sidebar.write(selected_search)

search_keyword = st.text_input(selected_search)
button_clicked = st.button("Search")


search_result = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    if selected_search == 'Songs/track':
        st.write("Search starts "+selected_search)
        results = sp.search(q='track:'+search_keyword, type='track', limit=20)
        tracks_in_album = results['tracks']['items']
        if len(tracks_in_album) > 0:
            for item in tracks_in_album:
                # st.write(item['name']+"   ....BY...  "+item['artists'][0]['name'])
                search_result.append(item['name']+"....BY..."+item['artists'][0]['name'])
                # st.write("Track ID:  "+item['id']+" -----  " + "Artists Id:  "+item['artists'][0]['id'])

    elif selected_search == 'Artists':
        st.write("Search starts "+selected_search)
        artists = sp.search(q='artist:'+search_keyword,
                            type='artist', limit=20)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for item in artists_list:
                # st.write(item['name'])
                search_result.append(item['name'])
                # st.write("Track ID:  "+item['id']+" -----  " + "Artists Id:  "+item['artists'][0]['id'])

    elif selected_search == 'Album':
        st.write("Search starts "+selected_search)
        albums = sp.search(q='album:'+search_keyword, type='album', limit=30)
        album_list = albums['albums']['items']
        if(len(album_list) > 0):
            for item in album_list:
                # st.write(item['name']+"&nbsp;....BY....&nbsp;"+'&nbsp;'+item['artists'][0]['name'])
                search_result.append(item['name']+"....BY..."+item['artists'][0]['name'])
                # st.write('Album Id:&nbsp;&nbsp;'+item['id']+'&nbsp;&nbsp;Artists Id:&nbsp;&nbsp;'+item['artists'][0]['id'])


selected_track = None
selected_artist = None
selected_album = None

if selected_search == 'Songs/track':
    selected_track = st.selectbox('choose your Songs/track : ', search_result)
elif selected_search == 'Artists':
    selected_artist = st.selectbox('choose your Artist : ', search_result)
elif selected_search == 'Album':
    selected_album = st.selectbox('choose your Album :', search_result)


if selected_track is not None and len(results) > 0:
    track_list = results['tracks']['items']
    track_id = None
    if len(track_list) > 0:
        for track in track_list:
            st_temp = track['name']+"....BY..."+track['artists'][0]['name']
            if selected_track == st_temp:
                track_id=track['id']
                track_album=track['album']['name']
                img_album=track['album']['images'][1]['url']
                song_recomandation.save_album_img(img_album,track_id)
                # st.write(track_id,track_album,img_album)
            # st.write(st_temp,selected_track)
    
        selected_track_choice=None


        if track_id is not None:
            image=song_recomandation.get_album_img(track_id)
            st.image(image)
            track_choice=['Fetures','Similar songs']
            selected_track_choice= st.sidebar.selectbox('Please select Track choice:',track_choice)

            if selected_track_choice=='Fetures':
                track_fetures=sp.audio_features(track_id)
                df=pd.DataFrame(track_fetures,index=[0])
                df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                st.dataframe(df_features)
                polar_plot.feature_plot(df_features)
            elif selected_track_choice=='Similar songs':
                token=song_recomandation.get_token(C_ID,C_SCR)
                similar_song_json=song_recomandation.get_track_recommendations(track_id,token)
                recomdation_list=similar_song_json['tracks']
                # st.write('Recomand...')
                recomdation_list_df=pd.DataFrame(recomdation_list)
                recomdation_df=recomdation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
                st.dataframe(recomdation_df)
                # song_recomandation.song_recomdation_vis()
                song_recomandation.song_recomdation_vis(recomdation_df)

        else:
            st.write("please select a track from list")

elif selected_album is not None and len(albums)>0:
    album_list=albums['albums']['items']
    album_id=None
    album_uri=None
    album_name=None
     
    if len(album_list)>0:
        for album in album_list:
            st_temp=album['name']+"....BY..."+album['artists'][0]['name']
            if st_temp==selected_album:
                album_id=album['id']
                album_uri=album['uri']
                album_name=album['name']
        if album_id is not None and album_uri is not None:

           

                st.write("COLLECTING ALL SONG OF ALBUMS :"+album_name)
                album_tracks=sp.album_tracks(album_id)
                df_album_track=pd.DataFrame(album_tracks['items'])
                # st.dataframe(df_album_track)
                df_album_min_track=df_album_track.loc[:,['id','name','duration_ms','explicit','preview_url']]
                # st.dataframe(df_album_min_track)
                for idx in df_album_min_track.index:
                    with st.container():
                        col1,col2,col3,col4=st.columns((4,4,2,2))
                        col5,col6=st.columns((8,2))
                        col1.write(df_album_min_track['id'][idx])
                        col2.write(df_album_min_track['name'][idx])
                        col3.write(df_album_min_track['duration_ms'][idx])
                        col4.write(df_album_min_track['explicit'][idx])
                       
                        if df_album_min_track['preview_url'] is not None:
                            col5.write(df_album_min_track['preview_url'][idx])
                            with col6:
                                st.audio(df_album_min_track['preview_url'][idx],format="audio/mp3")



if selected_artist is not None and len(artists)>0:
    artists_list=artists['artists']['items']
    artist_id=None
    artist_uri=None
    selected_artist_choice=None
    if len(artists_list)>0:
        for artist in artists_list:
             if selected_artist==artist['name']:
                 artist_id=artist['id']
                 artist_uri=artist['uri']

        if artist_id is not None:
            artist_choice=['Albums','Top Songs']
            selected_artist_choice = st.sidebar.selectbox("Enter Artist Choice: ",artist_choice)
        
        if selected_artist_choice is not None:
            if selected_artist_choice=='Albums':
                # st.write("Albums")
                artist_uri='spotify:artist:'+artist_id
                album_res=sp.artist_albums(artist_uri,album_type='album')
                all_albums=album_res['items']
                col1,col2,col3=st.columns((6,6,6))
                for album in all_albums:
                    col1.write(album['name'])
                    col2.write(album['release_date'])
                    col3.write(album['total_tracks'])

            elif selected_artist_choice=='Top Songs':
                # st.write("top Songs")
                artist_uri='spotify:artist:'+artist_id
                top_artist_song=sp.artist_top_tracks(artist_uri)
                for track in top_artist_song['tracks']:
                    with st.container():
                        col1,col2,col3,col4=st.columns((4,4,2,2))
                        col5,col6=st.columns((8,2))
                        col7,col8=st.columns((6,6))
                        col9,col10=st.columns((6,6))

                        col1.write(track['id'])
                        col2.write(track['name'])
                        # col3.write(track['duration_ms'])
                        # col4.write(track['popularity'])
                    
                        if track['preview_url'] is not None:
                            col5.write(track['preview_url'])
                            with col6:
                                st.audio(track['preview_url'],format="audio/mp3")
                        with col3:
                            def feature_requested():
                                track_features  = sp.audio_features(track['id']) 
                                df = pd.DataFrame(track_features, index=[0])
                                df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                                with col9:
                                  st.dataframe(df_features)
                                with col10:
                                  polar_plot.feature_plot(df_features)
                            
                            feature_button_state = st.button('Track Audio Features', key=track['id'], on_click=feature_requested)
                        with col4:
                            def similar_song_request():
                                token=song_recomandation.get_token(C_ID,C_SCR)
                                similar_song_json=song_recomandation.get_track_recommendations(track['id'],token)
                                recomdation_list=similar_song_json['tracks']
                                # st.write('Recomand...')
                                recomdation_list_df=pd.DataFrame(recomdation_list)
                                recomdation_df=recomdation_list_df[['name', 'explicit', 'duration_ms', 'popularity']]
                                st.dataframe(recomdation_df)
                                # song_recomandation.song_recomdation_vis()
                                song_recomandation.song_recomdation_vis(recomdation_df)

                                with col9:
                                    st.dataframe(recomdation_df)
                                with col10:
                                    song_recomandation.song_recomdation_vis(recomdation_df)
                  

                            similar_song_button= st.button('Similar Song ',key=track['id'],on_click=similar_song_request)

        else:
            st.write('please select a choice from a above list')
            

            
            

            

