import streamlit as st
import pickle
import pandas as pd
import requests
import json
import os

# TMDB API Key
TMDB_API_KEY = "e238291df5c32e4560562b40024779fd"


# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies


# Load movie data and similarity matrix
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))


# Function to fetch movies from TMDB API
def fetch_movies_from_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        return []


# Get TMDB poster URL
def get_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None


# Chatbot function
def chatbot_response(user_message):
    try:
        # Predefined genres mapping for TMDB API
        genres_mapping = {
            "action": 28,
            "comedy": 35,
            "drama": 18,
            "horror": 27,
            "romance": 10749,
            "sci-fi": 878,
            "thriller": 53,
        }

        # Default genre if none is specified
        genre_id = None
        for genre, tmdb_id in genres_mapping.items():
            if genre in user_message.lower():
                genre_id = tmdb_id
                break

        # Discover movies based on genre or fetch popular movies
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "sort_by": "popularity.desc",
        }
        if genre_id:
            params["with_genres"] = genre_id

        response = requests.get(url, params=params)
        data = response.json()
        results = data.get("results", [])

        posters = []
        recommendations = []
        for movie in results[:5]:  # Limit to top 5 movies
            title = movie.get("title", "Unknown Title")
            release_date = movie.get("release_date", "Unknown Year")
            poster_url = get_poster_url(movie.get("poster_path"))
            recommendations.append(f"{title} ({release_date[:4]})")
            posters.append((title, release_date[:4], poster_url))

        if recommendations:
            reply = "Here are some popular movies you might like:\n" + "\n".join(
                recommendations
            )
            return reply, posters
        else:
            return (
                "I couldn't find any movies matching your query. Please try again.",
                [],
            )

    except Exception as e:
        return f"Error: {e}", []


# Save user credentials
def save_user_credentials(username, password):
    user_data = {"username": username, "password": password}
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump([user_data], f)
    else:
        with open("users.json", "r") as f:
            existing_data = json.load(f)
        existing_data.append(user_data)
        with open("users.json", "w") as f:
            json.dump(existing_data, f)


# Authenticate user
def authenticate_user(username, password):
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
        for user in users:
            if user.get("username") == username and user.get("password") == password:
                return True
    return False


# Login/Register Page
def login_page():
    st.markdown(
        """
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: rgba(25, 42, 86, 0.92);
        }
        .stButton>button {
            background-color: rgba(39, 174, 96, 0.92);
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px;
        }
        .stTextInput>div>div>input {
            border: 1px solid rgba(52, 152, 219, 1); 
            background-color: rgba(40, 116, 166, 0.92); 
            padding: 8px;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Movie Recommendation System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
            else:
                st.error("Invalid credentials! Please try again.")

    with tab2:
        new_username = st.text_input("Choose a Username", key="register_username")
        new_password = st.text_input(
            "Choose a Password", type="password", key="register_password"
        )
        confirm_password = st.text_input(
            "Confirm Password", type="password", key="confirm_password"
        )

        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match! Please try again.")
            else:
                save_user_credentials(new_username, new_password)
                st.success("Registration successful! Please log in.")


# Main Recommender Page
def recommender_page():
    st.markdown(
        """
        <style>
        /* Background color for the entire app */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: rgba(25, 42, 86, 0.92);
        }

        /* Customize buttons */
        .stButton>button {
            background-color: rgba(39, 174, 96, 0.92);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }

        /* Customize input boxes */
        .stTextInput>div>div>input {
            border: 2px solid ;
            background-color: rgba(40, 116, 166, 0.92);
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }

        /* Customize selectbox */
        [data-baseweb="select"] {
            background-color: rgba(9, 237, 255, 0.92);
            border: 2px solid;
            border-radius: 5px;
        }

        /* Sidebar customization */
        [data-testid="stSidebar"] {
            background-color: rgba(33, 47, 90, 0.92);
            padding: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("Movie Recommendation System")
    st.subheader(f"Welcome, {st.session_state.username}!")

    # Movie recommendation system
    selected_movie_name = st.selectbox("Select a movie", movies["title"].values)
    if st.button("Recommend"):
        recommendations = recommend(selected_movie_name)
        st.write("Recommended Movies:")

        # Display recommendations with posters in a single row
        cols = st.columns(len(recommendations))
        for idx, movie in enumerate(recommendations):
            posters = fetch_movies_from_tmdb(movie)
            poster_url = None
            if posters:
                poster_url = get_poster_url(posters[0].get("poster_path"))

            with cols[idx]:
                if poster_url:
                    st.image(
                        poster_url, caption=movie, use_container_width=True
                    )  # Updated parameter
                else:
                    st.write(movie)

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None

    # Chatbot Toggle
    if st.button(
        (
            "Open Chatbot"
            if not st.session_state.get("show_chatbot", False)
            else "Close Chatbot"
        ),
        key="chatbot_toggle",
    ):
        st.session_state.show_chatbot = not st.session_state.show_chatbot

    # Chatbot Area
    if st.session_state.get("show_chatbot", False):
        st.markdown("### Chatbot")
        user_input = st.text_input("Ask the chatbot", key="chatbot_input")
        if st.button("Send", key="chatbot_send"):
            if user_input:
                response, posters = chatbot_response(user_input)

                # Only display response if no movies were found
                if not posters:
                    st.write(response)
                else:
                    st.write("Here are some movies you might like:")

                # Display posters if available
                if posters:
                    num_posters = len(posters)
                    cols = st.columns(num_posters)
                    for idx, (title, year, poster_url) in enumerate(posters):
                        with cols[idx]:
                            if poster_url:
                                st.image(
                                    poster_url,
                                    caption=f"{title} ({year})",
                                    use_container_width=True,
                                )
                            else:
                                st.write(f"{title} ({year})")


# Render appropriate page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False

if not st.session_state.authenticated:
    login_page()
else:
    recommender_page()
