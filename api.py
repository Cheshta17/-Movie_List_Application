import streamlit as st
import pandas as pd
import seaborn as sns

# Load the data from the CSV file into a DataFrame
data = pd.read_csv('movie_metadata.csv')

# Create a bar plot using seaborn
sns.barplot(x='imdb_score', y='movie_title', data=data.sort_values(by='imdb_score', ascending=False).head(10))

# Display the bar plot in the Streamlit app
st.pyplot()
