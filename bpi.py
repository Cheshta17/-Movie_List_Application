import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

# Load the data
@st.cache
def load_data():
    movies = pd.read_csv('tmdb_5000_movies.csv')
    credits = pd.read_csv('tmdb_5000_credits.csv')
    return movies, credits

# Load processed data and similarity matrix
@st.cache
def load_processed_data():
    new_df = pickle.load(open('movies_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return new_df, similarity

# Convert dict back to DataFrame
def dict_to_df(data_dict):
    return pd.DataFrame.from_dict(data_dict)

# Load data
movies, credits = load_data()
new_df, similarity = load_processed_data()
new_df = dict_to_df(new_df)

# Define the recommendation function
def recommend(movie):
    movie_idx = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = [new_df.iloc[i[0]].title for i in movie_list]
    return recommended_movies

# Streamlit app title
st.title('Movie Recommendation System')

# Movie selection
movie_list = new_df['title'].values
selected_movie = st.selectbox('Select a movie to get recommendations:', movie_list)

# Display recommendations
if st.button('Recommend'):
    recommendations = recommend(selected_movie)
    st.write('Top 5 recommended movies:')
    for movie in recommendations:
        st.write(movie)

# Additional EDA section
st.title('Movie Dataset Analysis')

# Show data
if st.checkbox('Show raw data'):
    st.write(movies.head())

# Plotting section
st.title('Visualizations')

# Top 10 Movies with Highest IMDB Score
if st.checkbox('Show Top 10 Movies with Highest IMDB Score'):
    top10_imdb = movies.sort_values(by='vote_average', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(y='title', x='vote_average', data=top10_imdb, palette='Blues', ax=ax)
    ax.set_title('Top 10 Movies with Highest IMDB Score')
    st.pyplot(fig)

# Top 10 Movies with Highest Profit
if st.checkbox('Show Top 10 Movies with Highest Profit'):
    movies['profit'] = movies['revenue'] - movies['budget']
    top10_profit = movies.sort_values(by='profit', ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(y='title', x='profit', data=top10_profit, palette='Blues', ax=ax)
    ax.set_title('Top 10 Movies with Highest Profit')
    st.pyplot(fig)

# Add more plots as needed, similar to the above blocks

# Ensure that the script is not run on import
if __name__ == "__main__":
    st.run()
