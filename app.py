import streamlit as st
import pickle
import pandas as pd
import requests
import os
import shutil
bigfile = "similar.pkl"

if not os.path.exists(bigfile): 
    with st.spinner("Downloading..."):
        # URL to a publicly accessible link
        url = "https://drive.google.com/uc?id=1nk1dQdq907O6_thlexQYG79N-GT8VepZ&export=download&confirm=yes"

        # Download and save
        with requests.get(url, stream=True) as r, open(bigfile, "wb") as f:
            shutil.copyfileobj(r.raw, f)

base_url="https://api.jikan.moe/v4/"

def get_image(id):
    url=f"{base_url}anime/{id}/full"
    res=requests.get(url)
    ani=res.json()
    image=ani['data']['images']['jpg']['image_url']
    return image

anime=pickle.load(open('anime_di.pkl','rb'))
anime_d=pd.DataFrame(anime)

sim=pickle.load(open(bigfile,'rb'))
#sim=pd.read_pickle(bigfile)


def search(movie):
    for z in range(len(anime_d['alt_title'])): #parse through each row by index
        for i, j in enumerate(set(anime_d['alt_title'].iloc[z])): #convert to set, give indices to match the values into i,j
            if j == movie: #compare values
                idx=z
    return idx

def recommend(a_name):
    idx=anime_d[anime_d['title']==a_name].index[0]
    dist=sim[idx]
    anime_list=sorted(list(enumerate(dist)),reverse=True, key=lambda x:x[1])[1:6] #only top 5 values
    print(anime_list)
    recommended=[]
    images=[]
    for k in anime_list:
        i_list=(anime_d.iloc[k[0]].anime_id)
        images.append(get_image(i_list))
    for i in anime_list:
        recommended.append(anime_d.iloc[i[0]].title) #to only print indexes
    return recommended,images


st.title('Anime Recommender System')

with st.form(key='user_form'):
    st.markdown('Enter the anime name to search in database')
    anime_name=st.text_input(label='Anime Name')
    
    button=st.form_submit_button(label='Search Database')

    if button:
        z=search(anime_name)
        pos= anime_d.iloc[z].title
        st.warning(f"Official Title: {pos}")


a_name=st.selectbox('What anime have you recently watched?',anime_d['title'])

button2=st.button(label='Find Similar')

if button2:
    col1,col2,col3,col4,col5=st.columns(5)
    rec,images=recommend(a_name)
    
    with col1:
        st.text(rec[0])
        st.image(images[0])
    
    with col2:
        st.text(rec[1])
        st.image(images[1])

    with col3:
        st.text(rec[2])
        st.image(images[2])

    with col4:
        st.text(rec[3])
        st.image(images[3])
        
    with col5:
        st.text(rec[4])
        st.image(images[4])


