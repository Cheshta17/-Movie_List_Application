import streamlit as st
import pandas as pd
import pickle

# Load the movie data
data = pd.read_csv('movie_metadata.csv')

# Load the pre-computed data
with open('genres_data.pkl', 'rb') as f:
    genres = pickle.load(f)

# Load the recommendation engine
with open('recommendation_engine.pkl', 'rb') as f:
    recommendation_engine = pickle.load(f)

# Streamlit app
st.title("Movie Recommender System")

# Get user input for the movie
selected_movie = st.selectbox("Select a movie", data['movie_title'].values)

# Recommend movies
if st.button("Recommend"):
    recommendations = recommendation_engine(selected_movie)
    for i, movie in enumerate(recommendations.index[:10]):
        st.write(f"{i+1}. {movie}")

# Additional functionality (if needed)
# ...
