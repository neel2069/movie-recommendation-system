import streamlit as st
from movie_recommender import (
    get_recommendations,
    fetch_poster
)

# Page configuration
st.set_page_config(
    page_title="CINEAI",
    page_icon="🎬",
    layout="wide"
)

# Initialize watchlist
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Header
st.markdown(
    """
    <h1 style='text-align:center;
    color:#FF4B4B;
    font-size:50px;'>
    🎬 CINEAI
    </h1>

    <p style='text-align:center;
    font-size:20px;'>
    Discover movies you'll love using AI
    </p>
    """,
    unsafe_allow_html=True
)

# Sidebar controls
st.sidebar.title("⚙️ Controls")

num_movies = st.sidebar.slider(
    "Number of recommendations",
    1,
    10,
    5
)

show_overview = st.sidebar.checkbox(
    "Show movie overview",
    True
)

# Show watchlist
st.sidebar.subheader("📌 Watchlist")

if st.session_state.watchlist:
    for movie in st.session_state.watchlist:
        st.sidebar.write(movie)
else:
    st.sidebar.write("No movies added yet")

# Search input
movie_name = st.text_input(
    "🔍 Search movie",
    placeholder="Type movie name like Interstellar"
)

# Recommend button
if st.button("🎬 Recommend Movies"):

    if movie_name:

        with st.spinner(
            "Finding best movies..."
        ):

            movies, scores = (
                get_recommendations(
                    movie_name
                )
            )

        if movies:

            st.subheader(
                "Recommended Movies"
            )

            cols = st.columns(
                num_movies
            )

            for i in range(
                min(
                    num_movies,
                    len(movies)
                )
            ):

                poster, rating, overview = (
                    fetch_poster(
                        movies[i]
                    )
                )

                with cols[i]:

                    if poster:

                        st.image(
                            poster,
                            use_container_width=True
                        )

                    st.markdown(
                        f"### {movies[i]}"
                    )

                    st.write(
                        f"⭐ Rating: {rating}"
                    )

                    st.write(
                        f"📊 Match: {scores[i]}%"
                    )

                    if show_overview:

                        st.caption(
                            overview[:150]
                        )

                    # Watchlist button
                    if st.button(
                        f"Add to Watchlist {i}"
                    ):

                        if movies[i] not in st.session_state.watchlist:

                            st.session_state.watchlist.append(
                                movies[i]
                            )

                            st.success(
                                "Added to watchlist"
                            )

        else:

            st.error(
                "Movie not found in dataset"
            )

    else:

        st.warning(
            "Please enter a movie name"
        )

# Footer
st.markdown(
    """
    ---
    Made with ❤️ using Streamlit
    """
)