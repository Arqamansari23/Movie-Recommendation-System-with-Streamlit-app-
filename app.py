import  streamlit as st
import pickle
import pandas as pd
import requests

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))



def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # index of movie
    distances = sorted(list(enumerate(similarity[index])), reverse=True,
                       key=lambda x: x[1])  # all the sorted distances
    recommended_movies=[]
    recommended_movie_posters = []
    for i in distances[1:6]:  # because we need only Top 5 distances
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title) # print the Title of movie
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movie_posters


st.title('Movie Recommendation System ')
movie_selected = st.selectbox(
    'Select Movie To Be Recommended ?',
    movies['title'].values)



if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(movie_selected)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

