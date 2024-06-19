import pickle
import streamlit as st

# Load the data from pickle files
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

with open('eda.pkl', 'rb') as f:
    eda = pickle.load(f)

with open('genres.pkl', 'rb') as f:
    genres = pickle.load(f)

with open('x.pkl', 'rb') as f:
    x = pickle.load(f)

st.title("Movie Recommender")

# Create a dropdown menu for selecting a movie
movie_title = st.selectbox("Select a movie:", data['movie_title'].unique())

# Create a button to recommend similar movies
if st.button("Recommend"):
    # Call the recommendation function
    similar_movies = recommendation_movie(movie_title)
    st.write("Similar movies:")
    st.write(similar_movies.head(20))

def recommendation_movie(movie):
    movie = x[movie+'\xa0']
    similar_movies = x.corrwith(movie)
    similar_movies = similar_movies.sort_values(ascending=False)
    similar_movies = similar_movies.iloc[1:]
    return similar_movies.head(20)
