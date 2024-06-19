import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    for i in movie_list:
        # movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Enter a movie name', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)