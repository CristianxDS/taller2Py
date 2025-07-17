import praw
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

reddit = praw.Reddit(
    client_id="Omv8li5KJSBZsdiLzTkcBQ",
    client_secret="pV-62uWfgva18a-7RNp7uc7lK41WXg",
    user_agent="AnalisisReddit (por /u/LowIndependence7659)",
)
# Función para extraer datos de Reddit
def extract_reddit_data(subreddit_name, limit=100):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.hot(limit=limit)
    
    data = []
    for post in top_posts:
        data.append({
            "title": post.title,
            "score": post.score,
            "num_comments": post.num_comments,
            "author": post.author.name,
            "url": post.url,
            "created_utc": post.created_utc
        })
    return pd.DataFrame(data)

# Función para realizar análisis estadístico
def analyze_data(df):
    avg_score = df["score"].mean()
    max_score = df["score"].max()
    min_score = df["score"].min()
    
    st.write(f"Promedio de Score: {avg_score}")
    st.write(f"Máximo Score: {max_score}")
    st.write(f"Mínimo Score: {min_score}")
    
    # Distribución de Scores
    st.write("### Distribución de Scores")
    fig, ax = plt.subplots()
    sns.histplot(df["score"], kde=True, ax=ax)
    st.pyplot(fig)

# Función principal de Streamlit
def main():
    st.title("Análisis de Tendencias en Reddit")
    
    subreddit_name = st.text_input("Nombre del Subreddit", "technology")
    limit = st.slider("Número de Posts a Extraer", 10, 200, 100)
    
    if st.button("Extraer y Analizar Datos"):
        df = extract_reddit_data(subreddit_name, limit)
        st.write("### Datos Extraídos")
        st.dataframe(df)
        
        st.write("### Análisis Estadístico")
        analyze_data(df)

if __name__ == "__main__":
    main()