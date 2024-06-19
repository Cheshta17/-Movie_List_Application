import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')
pd.options.display.max_columns = 50

# Load the dataset
data = pd.read_csv('movie_metadata.csv')

# Data preprocessing
data.drop_duplicates(inplace=True)
data.dropna(inplace=True)
data['title_year'] = data['title_year'].astype(int)
data['profit'] = (data['gross'] - data['budget']) / 1e6  # Convert profit to million

# Create a copy for EDA
eda = data.copy()

# Define functions for interactive widgets
def duration_type(x, quantiles):
    q1, q3 = quantiles
    if x >= q3:
        return 'long'
    elif x >= q1:
        return 'medium'
    else:
        return 'short'

eda['duration_type'] = eda['duration'].apply(lambda x: duration_type(x, eda['duration'].quantile([0.33, 0.66])))
eda['languages'] = np.where(eda['language'] == 'English', 'English', 'Foreign')

# Streamlit app
st.title('Movie Data Analysis')

# Top 10 Movies with Highest IMDB Score
st.header('Top 10 Movies with Highest IMDB Score')
top10_imdb = eda.sort_values(by='imdb_score', ascending=False).head(10)
st.bar_chart(top10_imdb[['movie_title', 'imdb_score']].set_index('movie_title'))

# Top 10 Movies with Highest Profit
st.header('Top 10 Movies with Highest Profit')
top10profit = eda[['profit', 'movie_title']].sort_values(by='profit', ascending=False).head(10)
st.bar_chart(top10profit.set_index('movie_title'))

# Top 10 Movies with Highest Loss
st.header('Top 10 Movies with Highest Loss')
loss = eda[['profit', 'movie_title']].sort_values(by='profit', ascending=True).head(10)
st.bar_chart(loss.set_index('movie_title'))

# Group by Language
st.header('Gross and Profit by Language')
gross_lang = eda.groupby('languages').agg(gross_sum=('gross','sum'), gross_mean=('gross','mean')).reset_index()
profit_lang = eda.groupby('languages').agg(profit_sum=('profit','sum'), profit_mean=('profit','mean')).reset_index()

st.write('Gross by Language')
st.dataframe(gross_lang)
st.write('Profit by Language')
st.dataframe(profit_lang)

# Duration analysis
st.header('Profit by Duration Type')
profit_duration = eda.groupby('duration_type').agg(profit_sum=('profit','sum'), profit_mean=('profit','mean')).reset_index()
st.bar_chart(profit_duration.set_index('duration_type'))

# Group by Genre
eda['genre1'] = eda['genres'].str.split('|').apply(lambda x: x[0])
gross_genre = eda.groupby('genre1').agg(gross_sum=('gross','sum'), gross_mean=('gross','mean')).reset_index()
profit_genre = eda.groupby('genre1').agg(profit_sum=('profit','sum'), profit_mean=('profit','mean')).reset_index()
imdb_genre = eda.groupby('genre1').agg(imdb_score=('imdb_score','mean')).reset_index()

st.header('Analysis by Genre')
st.write('Gross by Genre')
st.bar_chart(gross_genre.set_index('genre1'))

st.write('Profit by Genre')
st.bar_chart(profit_genre.set_index('genre1'))

st.write('IMDB Score by Genre')
st.bar_chart(imdb_genre.set_index('genre1'))

# Interactive widgets for language and director
st.header('Interactive Analysis')

st.subheader('Top Movies by Language')
language = st.selectbox('Select Language', eda['language'].unique())
st.dataframe(eda[eda['language'] == language][['movie_title', 'imdb_score']].sort_values(by='imdb_score', ascending=False).head(10))

st.subheader('Top Movies by Director')
director = st.selectbox('Select Director', eda['director_name'].unique())
st.dataframe(eda[eda['director_name'] == director][['movie_title', 'title_year', 'imdb_score']].sort_values(by='imdb_score', ascending=False).head(10))

# Movie recommendation system
st.header('Movie Recommendation System')
movie = st.selectbox('Select a Movie', eda['movie_title'].unique())

# Prepare genres for recommendation
from mlxtend.preprocessing import TransactionEncoder

x = eda['genres'].str.split('|')
te = TransactionEncoder()
x = te.fit_transform(x)
x = pd.DataFrame(x, columns = te.columns_)
genres = x.astype('int')
genres.insert(0, 'movie_title', eda['movie_title'])
genres = genres.set_index('movie_title')

def recommendation_movie(movie_title):
    movie = genres.loc[movie_title]
    similar_movies = genres.corrwith(movie, axis=1)
    similar_movies = similar_movies.sort_values(ascending=False).iloc[1:]
    return similar_movies.head(10)

recommendations = recommendation_movie(movie)
st.write('Recommendations for', movie)
st.dataframe(recommendations)

# Run Streamlit app
if __name__ == '__main__':
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
