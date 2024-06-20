import pandas as pd
import streamlit as st
@st.cache_data()
def load_data():
    data = pd.read_csv('movie_metadata.csv')
    return data

data = load_data()
def show_all_movies():
    st.write(data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])
def add_new_movie():
    movie_title = st.text_input("Enter Movie Title")
    director_name = st.text_input("Enter Director Name")
    title_year = st.number_input("Enter Release Year", min_value=1900, max_value=2024, step=1)
    language = st.text_input("Enter Language")
    imdb_score = st.number_input("Enter IMDB Score", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Add Movie"):
        new_movie = {'movie_title': movie_title, 'director_name': director_name, 'title_year': title_year, 'language': language, 'imdb_score': imdb_score}
        data.loc[len(data)] = new_movie
        st.success("Movie added successfully!")
def filter_movies():
    filter_option = st.selectbox("Select Filter Option", ["Filter by Name", "Filter by Director", "Filter by Release Year", "Filter by Language", "Filter by Rating"])

    if filter_option == "Filter by Name":
        movie_name = st.text_input("Enter Movie Name")
        filtered_data = data[data['movie_title'].str.contains(movie_name, case=False)]
        st.write(filtered_data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])

    elif filter_option == "Filter by Director":
        director_name = st.text_input("Enter Director Name")
        filtered_data = data[data['director_name'].str.contains(director_name, case=False)]
        st.write(filtered_data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])

    # Add similar conditions for other filter options
def search_movie():
    movie_name = st.text_input("Enter Movie Name")
    filtered_data = data[data['movie_title'].str.contains(movie_name, case=False)]
    st.write(filtered_data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])
def update_movie():
    movie_name = st.text_input("Enter Movie Name to Update")
    filtered_data = data[data['movie_title'].str.contains(movie_name, case=False)]

    if not filtered_data.empty:
        movie_index = filtered_data.index[0]
        st.write("Current Details:")
        st.write(filtered_data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])

        new_director = st.text_input("Enter New Director Name (Leave blank if no change)")
        new_year = st.number_input("Enter New Release Year (Leave 0 if no change)", min_value=1900, max_value=2024, step=1)
        new_language = st.text_input("Enter New Language (Leave blank if no change)")
        new_rating = st.number_input("Enter New IMDB Score (Leave 0.0 if no change)", min_value=0.0, max_value=10.0, step=0.1)

        if new_director:
            data.at[movie_index, 'director_name'] = new_director
        if new_year:
            data.at[movie_index, 'title_year'] = new_year
        if new_language:
            data.at[movie_index, 'language'] = new_language
        if new_rating:
            data.at[movie_index, 'imdb_score'] = new_rating

        st.success("Movie details updated successfully!")
    else:
        st.warning("No movie found with the given name.")
def delete_movie():
    movie_name = st.text_input("Enter Movie Name to Delete")
    filtered_data = data[data['movie_title'].str.contains(movie_name, case=False)]

    if not filtered_data.empty:
        movie_index = filtered_data.index[0]
        st.write("Movie to be deleted:")
        st.write(filtered_data[['movie_title', 'director_name', 'title_year', 'language', 'imdb_score']])

        if st.button("Confirm Delete"):
            data.drop(movie_index, inplace=True)
            st.success("Movie deleted successfully!")
    else:
        st.warning("No movie found with the given name.")
def main():
    st.title("Movie List Application")

    menu = ["Show All Movies", "Add New Movie", "Filter Movies", "Search Movie", "Update Movie", "Delete Movie"]
    choice = st.sidebar.selectbox("Select an Option", menu)

    if choice == "Show All Movies":
        show_all_movies()
    elif choice == "Add New Movie":
        add_new_movie()
    elif choice == "Filter Movies":
        filter_movies()
    elif choice == "Search Movie":
        search_movie()
    elif choice == "Update Movie":
        update_movie()
    elif choice == "Delete Movie":
        delete_movie()

if __name__ == "__main__":
    main()
