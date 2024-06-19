import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('movie_metadata.csv')
    return data

# Preprocess the data
def preprocess_data(data):
    data.dropna(inplace=True)
    data['title_year'] = data['title_year'].astype(int)
    x = data['genres'].str.split('|')
    te = TransactionEncoder()
    x = te.fit_transform(x)
    x = pd.DataFrame(x, columns=te.columns_)
    genres = x.astype('int')
    genres.insert(0, 'movie_title', data['movie_title'])
    genres = genres.set_index('movie_title')
    return genres

# Recommendation function
def recommendation_movie(movie, x):
    movie = x[movie + '\xa0']
    similar_movies = x.corrwith(movie)
    similar_movies = similar_movies.sort_values(ascending=False)
    similar_movies = similar_movies.iloc[1:]
    return similar_movies.head(20)

def main():
    # Load the data
    data = load_data()

    # Preprocess the data
    genres = preprocess_data(data)

    # Add a title
    st.title("Movie Recommendation System")

    # Add a dropdown to select the movie
    movie_list = list(data['movie_title'].sort_values().values)
    selected_movie = st.selectbox("Select a movie:", movie_list)

    # Recommend similar movies
    if st.button("Recommend"):
        recommendations = recommendation_movie(selected_movie, genres.transpose())
        st.subheader(f"Similar movies to '{selected_movie}':")
        st.table(recommendations)

if __name__ == "__main__":
    main()
