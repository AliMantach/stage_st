import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Movie Database",
    page_icon="🎬",
    layout="wide"
)

st.title("Movie Database Explorer")
st.markdown("Search for movie information using the OMDB API")
st.markdown("Search for covid stats")

# API key input
api_key = st.text_input("Enter your OMDB API key", 
                        help="Get your free API key at https://www.omdbapi.com/apikey.aspx")

# Search options
search_type = st.radio(
    "Search type",
    ["Movie Title", "Movie ID (IMDb ID)"],
    horizontal=True
)

if search_type == "Movie Title":
    search_term = st.text_input("Enter movie title", "The Matrix")
    search_year = st.text_input("Year (optional)", "")
    search_params = {"s": search_term}
    if search_year:
        search_params["y"] = search_year
else:
    search_term = st.text_input("Enter IMDb ID", "tt0133093")
    search_params = {"i": search_term}

# Plot option for single movie search
if search_type == "Movie ID (IMDb ID)":
    include_plot = st.checkbox("Include full plot", value=True)
    if include_plot:
        search_params["plot"] = "full"

if st.button("Search Movies"):
    if not api_key:
        st.error("Please enter your OMDB API key")
    else:
        try:
            # Make API request
            url = f"https://www.omdbapi.com/?apikey={api_key}"
            for key, value in search_params.items():
                url += f"&{key}={value}"
                
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                
                if data.get("Response") == "False":
                    st.error(f"Error: {data.get('Error', 'Unknown error')}")
                else:
                    # Display results
                    if "Search" in data:
                        
                        st.subheader(f"Found {len(data['Search'])} results for '{search_term}'")
                        
                        # Convert to DataFrame
                        movies_df = pd.DataFrame(data["Search"])
                        st.dataframe(movies_df)
                        
                        # Option to download results
                        csv = movies_df.to_csv(index=False)
                        st.download_button(
                            label="Download results as CSV",
                            data=csv,
                            file_name=f"movie_search_{search_term}.csv",
                            mime="text/csv"
                        )
                        
                        # Display details for a selected movie
                        if not movies_df.empty:
                            st.subheader("View Details")
                            selected_movie = st.selectbox(
                                "Select a movie to view details",
                                movies_df["Title"].tolist()
                            )
                            
                            selected_id = movies_df[movies_df["Title"] == selected_movie]["imdbID"].iloc[0]
                            
                            if st.button("View Details"):
                                detail_url = f"https://www.omdbapi.com/?apikey={api_key}&i={selected_id}&plot=full"
                                detail_response = requests.get(detail_url)
                                
                                if detail_response.status_code == 200:
                                    movie_data = detail_response.json()
                                    display_movie_details(movie_data)
                                else:
                                    st.error("Failed to fetch movie details")
                    
                    else:
                     
                        display_movie_details(data)
                        
                        
                        st.session_state.last_movie = data
                        
            else:
                st.error(f"Error: Status code {response.status_code}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

def display_movie_details(movie):
    """Display details for a single movie"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if movie.get("Poster") != "N/A":
            st.image(movie["Poster"], width=300)
        else:
            st.markdown("*No poster available*")
    
    with col2:
        st.subheader(movie["Title"])
        st.markdown(f"**Year:** {movie.get('Year', 'N/A')}")
        st.markdown(f"**Rated:** {movie.get('Rated', 'N/A')}")
        st.markdown(f"**Released:** {movie.get('Released', 'N/A')}")
        st.markdown(f"**Runtime:** {movie.get('Runtime', 'N/A')}")
        st.markdown(f"**Genre:** {movie.get('Genre', 'N/A')}")
        st.markdown(f"**Director:** {movie.get('Director', 'N/A')}")
        st.markdown(f"**Writer:** {movie.get('Writer', 'N/A')}")
        st.markdown(f"**Actors:** {movie.get('Actors', 'N/A')}")
    
    st.subheader("Plot")
    st.write(movie.get("Plot", "No plot available"))
    
    st.subheader("Ratings")
    if "Ratings" in movie and movie["Ratings"]:
        ratings_df = pd.DataFrame(movie["Ratings"])
        st.dataframe(ratings_df)
    else:
        st.write("No ratings available")
    
  
    with st.expander("Additional Information"):
        st.markdown(f"**Box Office:** {movie.get('BoxOffice', 'N/A')}")
        st.markdown(f"**Production:** {movie.get('Production', 'N/A')}")
        st.markdown(f"**Website:** {movie.get('Website', 'N/A')}")
        st.markdown(f"**IMDb Rating:** {movie.get('imdbRating', 'N/A')}")
        st.markdown(f"**IMDb Votes:** {movie.get('imdbVotes', 'N/A')}")
    
    movie_df = pd.json_normalize(movie)
    csv = movie_df.to_csv(index=False)
    st.download_button(
        label="Download movie details as CSV",
        data=csv,
        file_name=f"movie_{movie['imdbID']}.csv",
        mime="text/csv"
    )
