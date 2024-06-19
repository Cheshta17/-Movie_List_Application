import pandas as pd
import streamlit as st

# Assuming you have loaded your data using pd.read_csv("movie_metadata.csv")
# and assigned it to the variable 'data'

# Function to find top movies by IMDb score (assuming 'imdb_score' and 'movie_title' columns exist)
def top_imdb_movies(data, n=10):
    """Returns the top n movies with the highest IMDb score."""

    # Sort by descending IMDb score and select the top n rows
    top_movies = data.sort_values(by="imdb_score", ascending=False).head(n)

    # Select relevant columns for display
    top_movies_df = top_movies[["movie_title", "imdb_score"]]  # Adjust columns as needed

    # Return a DataFrame suitable for st.dataframe
    return top_movies_df

# Streamlit App Structure
st.title("Movie Exploration App")
st.write("This app allows you to explore various aspects of the movie dataset.")

# Section for Top Movies by IMDb Score
st.header("Top Movies by IMDb Score")
try:
    # Use a copy to avoid modifying original data
    top_movies_data = top_imdb_movies(data.copy())
    st.dataframe(top_movies_data)
except Exception as e:
    st.error("An error occurred while processing data:")
    st.write(e)  # Display the error message for debugging

# ... (add more sections for other analyses and visualizations)

