import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Your TMDB API Key
TMDB_API_KEY = "c34b0568c6401500afa560dea93da82f"


# Function to fetch movie poster, rating, and overview
def fetch_poster(movie_title):

    try:

        url = (
            "https://api.themoviedb.org/3/search/movie"
            f"?api_key={TMDB_API_KEY}"
            f"&query={movie_title}"
        )

        response = requests.get(url)

        data = response.json()

        if len(data["results"]) > 0:

            poster_path = data["results"][0]["poster_path"]

            rating = data["results"][0]["vote_average"]

            overview = data["results"][0]["overview"]

            if poster_path:

                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

                return poster_url, rating, overview

        return None, 0, "No overview available"

    except Exception as e:

        print("API Error:", e)

        return None, 0, "Error fetching data"
# Function to load movie dataset

@st.cache_data
def create_movie_data():

    print("Loading dataset...")  # This will print only once

    df = pd.read_csv(
        "tmdb_5000_movies.csv"
    )

    # Fill missing values
    df["overview"] = df[
        "overview"
    ].fillna("")

    # Remove duplicate titles
    df = df.drop_duplicates(
        subset="title"
    )

    # Reset index
    df = df.reset_index(
        drop=True
    )

    return df

# Function to get movie recommendations
def get_recommendations(movie_title):

    df = create_movie_data()

    # Convert titles to lowercase
    df["title"] = df["title"].str.lower()

    movie_title = movie_title.lower()

    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(
        df["overview"]
    )

    cosine_sim = cosine_similarity(
        tfidf_matrix,
        tfidf_matrix
    )

    indices = pd.Series(
        df.index,
        index=df["title"]
    ).drop_duplicates()

    # Fix: case-insensitive search
    if movie_title not in indices:

        return [], []

    idx = indices[movie_title]

    sim_scores = list(
        enumerate(cosine_sim[idx])
    )

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    sim_scores = sim_scores[1:6]

    movie_indices = [
        i[0] for i in sim_scores
    ]

    titles = df["title"].iloc[
        movie_indices
    ].str.title().tolist()

    scores = [
        round(i[1] * 100, 1)
        for i in sim_scores
    ]

    return titles, scores