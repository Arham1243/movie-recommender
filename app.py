import streamlit as st
import pickle
import pandas as pd
import requests
from io import BytesIO


movie_dict = pickle.load(open("pkl-files/movie_dict.pkl","rb"))
movies = pd.DataFrame(movie_dict)
similarity_url = "https://demo-designprojects.com/demo/test/similarity.pkl"

response = requests.get(similarity_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Load the pickle file from the response content
    similarity = pickle.loads(response.content)
    # Now you can use the loaded data as needed
else:
    # Handle the case where the request was not successful
    print("Failed to download the pickle file.")
# similarity= pickle.load(open("https://demo-designprojects.com/demo/test/similarity.pkl","rb"))

def get_movie_poster(movie_title):
    api_key = '99f3b2c3'
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    poster_url = data.get('Poster', '')
    return poster_url

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for movie in movies_list:
        movie_name = movies.iloc[movie[0]].title
        recommended_movies.append(movie_name)
        poster_url = get_movie_poster(movie_name) or "images/placeholder.jpg"
        recommended_movies_posters.append(poster_url)
    return recommended_movies,recommended_movies_posters


st.set_page_config(
    page_title="Movie Recommendation: Find Related Films",
    page_icon="🎥",
    layout="wide",
)



st.title("Discover Related Movies")
selected_movie = st.selectbox(
    "Enter your favorite movie name and click 'Recommend' to discover five related movie suggestions!",
    movies['title'].values)

if st.button('Recommend'):
    st.title("Recommended Movies")
    recommended_movies,posters = recommend(selected_movie)

    col1, col2, col3 , col4 ,col5 = st.columns(5,gap="medium")

    with col1:
        st.image(posters[0])
        st.subheader(recommended_movies[0])
    with col2:
        st.image(posters[1])
        st.subheader(recommended_movies[1])
    with col3:
        st.image(posters[2])
        st.subheader(recommended_movies[2])
    with col4:
        st.image(posters[3])
        st.subheader(recommended_movies[3])
    with col5:
        st.image(posters[4])
        st.subheader(recommended_movies[4])
