
import streamlit as st
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if TMDB_API_KEY is None:
    st.error("TMDB API key missing. Check .env file")
    st.stop()




#Dark mode toggle
dark_mode = st.toggle("🌙 Dark Mode", value=True)

if dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: white; }
        </style>
    """, unsafe_allow_html=True)


# ---------------- TMDB POSTER FUNCTION ----------------
#API_KEY = "ec76b2c94285e1ad9f158e2df1f8e164"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"

    data = response.json()
    poster_path = data.get("poster_path")

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# ---------------- RECOMMENDATION FUNCTION ----------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # <-- CHANGE HERE
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ---------------- LOAD DATA ----------------
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- UI ----------------
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.write(names[i])


##Optimizing speed of streamlit
@st.cache_data
def load_movies():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    return pd.DataFrame(movies_dict)

@st.cache_resource
def load_similarity():
    return pickle.load(open('similarity.pkl', 'rb'))

movies = load_movies()
similarity = load_similarity()

