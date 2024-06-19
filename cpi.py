import pickle
import streamlit as st
import pandas as pd

# Load the data from csv file
data = pd.read_csv('movie_metadata.csv')

# Perform data preprocessing and feature engineering
eda = data.copy()
eda['title_year'] = eda['title_year'].astype(int)
eda['profit'] = eda['gross'] - eda['budget']
eda['profit'] = round(eda['profit']/1000000,2)
eda['genres'] = eda['genres'].str.split('|')
eda['genre1'] = eda['genres'].apply(lambda x: x[0])
eda['genre2'] = eda['genres'].apply(lambda x: x[1] if len(x) > 1 else x[0])
eda['genre3'] = eda['genres'].apply(lambda x: x[2] if len(x) > 2 else x[0])
eda['genre4'] = eda['genres'].apply(lambda x: x[3] if len(x) > 3 else x[0])
eda['genre5'] = eda['genres'].apply(lambda x: x[5] if len(x) > 5 else x[0])

# Create a transaction encoder for genres
from mlxtend.preprocessing import TransactionEncoder
x = eda['genres'].str.split('|')
te = TransactionEncoder()
x = te.fit_transform(x)
x = pd.DataFrame(x, columns = te.columns_)
x.insert(0, 'movie_title', eda['movie_title'])
x = x.set_index('movie_title')

# Create a Streamlit app
st.title("Movie Recommender")

# Create a dropdown menu for selecting a movie
movie_title = st.selectbox("Select a movie:", x.index.unique())

# Create a button to recommend similar movies
if st.button("Recommend"):
    # Call the recommendation function
    similar_movies = recommendation_movie(movie_title)
    st.write("Similar movies:")
    st.write(similar_movies.head(20))

def recommendation_movie(movie):
    movie = x.loc[movie]
    similar_movies = x.corrwith(movie)
    similar_movies = similar_movies.sort_values(ascending=False)
    similar_movies = similar_movies.iloc[1:]
    return similar_movies.head(20)
