import streamlit as st
import pickle
import bz2file as bz2

import requests
import os
from dotenv import load_dotenv
load_dotenv()

st.title("Movie Recommender System")

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as f:
        data = pickle.load(f)
    return data


# movies = pickle.load(open('movies_list.pkl','rb'))
# similarity = pickle.load(open('similarity.pbz2','rb'))

movies = decompress_pickle('movies_list.pbz2')
similarity = decompress_pickle('similarity.pbz2')


API_KEY = os.environ.get("TMDB_API_KEY")

def fetch_poster(movie_id):
    base_url = "https://api.themoviedb.org/3/movie/"
    endpoint = f"{base_url}{movie_id}?api_key={API_KEY}"
    
    response = requests.get(endpoint)

    data = response.json()
    # st.write(data)
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']
    # st.write(response.text)

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x : x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters =[]
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        # Fetching posters from api using movie id
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies,recommended_movies_posters
    


selected_movie = st.selectbox(
   "Select the movie",
    movies['title'].values,
    index=None
)


if st.button("Recommend"):
    try:   
        # st.success(f'Recommended movies for {selected_movie}')
        names,posters = recommend(selected_movie)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            
            st.image(posters[0])
            st.write(names[0])

        with col2:
            
            st.image(posters[1])
            st.write(names[1])

        with col3:
            
            st.image(posters[2])
            st.write(names[2])
        
        with col4:
            
            st.image(posters[3])
            st.write(names[3])
            
        with col5:
            
            st.image(posters[4])
            st.write(names[4])
            
   
    except Exception as e:
        st.warning("Some error occured")