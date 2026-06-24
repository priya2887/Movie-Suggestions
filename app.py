import streamlit as st
import pickle
import pandas as pd
import requests

# Set page config
st.set_page_config(
    page_title="CineSuggest - AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Netflix/Cinematic Premium Styling
st.markdown("""
<style>
    .main {
        background-color: #111111;
        color: #ffffff;
    }
    .stApp {
        background-color: #111111;
    }
    h1 {
        color: #E50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    h3 {
        color: #F5F5F1 !important;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 300;
    }
    .stButton>button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: 0.3s ease all;
    }
    .stButton>button:hover {
        background-color: #ff1f2f !important;
        transform: scale(1.02);
    }
    .movie-card {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #333;
        min-height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .movie-title {
        color: #F5F5F1;
        font-size: 14px;
        font-weight: 600;
        margin-top: 10px;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except Exception:
        pass
    # Fallback to high-quality local-styled placeholder
    return f"https://via.placeholder.com/500x750/1a1a1a/ffffff?text=No+Poster"

# Load pickled models
@st.cache_resource
def load_data():
    import os
    try:
        base_dir = os.path.dirname(__file__)
        movie_dict_path = os.path.join(base_dir, "movie_dict.pkl")
        similarity_path = os.path.join(base_dir, "similarity.pkl")
        
        with open(movie_dict_path, "rb") as f:
            movie_dict = pickle.load(f)
        with open(similarity_path, "rb") as f:
            similarity = pickle.load(f)
        movies_df = pd.DataFrame(movie_dict)
        return movies_df, similarity
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return None, None

movies, similarity = load_data()

# App UI Header
st.markdown("<h1>🎬 CineSuggest</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI-Powered Content-Based Movie Recommendation System</h3>", unsafe_allow_html=True)

if movies is not None and similarity is not None:
    # Select box with all movies
    movie_list = movies['title'].values
    
    st.markdown("<div style='max-width: 600px; margin: 0 auto;'>", unsafe_allow_html=True)
    selected_movie = st.selectbox(
        "Type or select a movie to get recommendations:",
        movie_list,
        index=0
    )
    
    col_btn_l, col_btn_c, col_btn_r = st.columns([1, 2, 1])
    with col_btn_c:
        recommend_clicked = st.button("Generate Recommendations")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if recommend_clicked:
        try:
            # Get index of selected movie
            movie_idx = movies[movies['title'] == selected_movie].index[0]
            distances = similarity[movie_idx]
            
            # Sort distances
            movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            
            # Fetch recommendations
            recommended_movies_names = []
            recommended_movies_posters = []
            
            for i in movies_list:
                m_id = movies.iloc[i[0]].movie_id
                m_title = movies.iloc[i[0]].title
                recommended_movies_names.append(m_title)
                recommended_movies_posters.append(fetch_poster(m_id))
            
            # Render recommendations in 5 columns
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                with col:
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{recommended_movies_posters[idx]}" style="width:100%; border-radius:6px; aspect-ratio:2/3; object-fit:cover;" />
                        <div class="movie-title">{recommended_movies_names[idx]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"An error occurred during recommendation: {e}")
else:
    st.warning("Please ensure movie_dict.pkl and similarity.pkl are in the project directory.")
